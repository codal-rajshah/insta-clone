import os
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.parsers import FileUploadParser

from django.db import transaction

from apps.users.forms import UserCreationForm
from apps.users.models import User, UserProfile
from apps.users.serializers import UserSerializer, UserProfileSerializer


class UserCreationView(APIView):
    """
    To create user and their user profile
    """

    def post(self, request):
        """
        Creates the user in database
        """
        data = request.data

        user_form = UserCreationForm(data=data)
        if user_form.is_valid():
            with transaction.atomic():
                user = user_form.save()
                password = user_form.cleaned_data.get("password")
                user.set_password(password)
                user.save()

            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                user_form.errors, status=status.HTTP_400_BAD_REQUEST
            )


class UserViewSet(viewsets.ModelViewSet):
    """
    UserViewSet to update the authenticated user

    List the users
    Creates and updates the profile
    Updates the profile image if profile exists
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Only staff and superusers can see all the list of users
        """
        if self.action == "list":
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(
        detail=True, methods=["POST"], serializer_class=UserProfileSerializer
    )
    def profile(self, request, pk=None):
        """
        To create the user profile with required fields
        """
        data = request.data

        user = User.objects.get(pk=pk)
        data["user"] = pk

        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = None

        serializer_class = self.get_serializer_class()

        if profile is None:
            serializer = serializer_class(data=data)
        else:
            serializer = serializer_class(data=data, instance=profile)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=True,
        methods=["POST"],
        url_path="profile/image",
        parser_classes=[FileUploadParser],
    )
    def profile_image(self, request, pk=None):
        """
        Updates the profile picture of a user
        """
        file = request.data["file"]

        user = User.objects.get(pk=pk)

        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = None

        if profile is None:
            return Response(
                {
                    "success": False,
                    "detail": "Profile is not created for this user",
                }
            )

        if profile.profile_image is not None:
            try:
                os.remove(profile.profile_image.path)
            except (FileNotFoundError, ValueError):
                pass
        profile.profile_image = file
        profile.save()
        return Response({"success": True})
