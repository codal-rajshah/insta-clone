from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from django.contrib.auth import get_user_model
from django.db import transaction

from apps.friends.serializers import (
    FriendRequestSerializer,
    FriendRequestResponseSerializer,
    FriendSerializer,
)
from apps.friends.models import Friend, FriendRequest
from apps.friends.permissions import (
    FriendRequestOwnerPermission,
    FriendOwnerPermission,
)

User = get_user_model()


class FriendRequestViewSet(viewsets.ModelViewSet):
    """
    Viewsets to create and remove the friend request
    """

    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    queryset = FriendRequest.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return FriendRequestResponseSerializer
        else:
            return self.serializer_class

    def get_queryset(self):
        if self.action == "list":
            return FriendRequest.objects.filter(
                to_user=self.request.user, accepted=False
            )
        return FriendRequest.objects.all()

    @action(
        detail=True,
        methods=["POST"],
        url_path="accept",
        permission_classes=[FriendRequestOwnerPermission, IsAuthenticated],
    )
    def accept_request(self, request, pk=None):
        friend_request = FriendRequest.objects.get(pk=pk)
        self.check_object_permissions(self.request, friend_request)

        if not friend_request.accepted:
            friend_request.accepted = True
            friend_request.save()

            Friend.objects.create(
                user=friend_request.from_user, friend=friend_request.to_user
            )

        return Response({"success": True})

    @action(
        detail=True,
        methods=["POST"],
        url_path="reject",
        permission_classes=[FriendRequestOwnerPermission, IsAuthenticated],
    )
    def reject_request(self, request, pk=None):
        friend_request = FriendRequest.objects.get(pk=pk)
        self.check_object_permissions(self.request, friend_request)

        if Friend.objects.filter(
            user=friend_request.from_user, friend=friend_request.to_user
        ).exists():
            return Response(
                {"success": False}, status=status.HTTP_400_BAD_REQUEST
            )

        friend_request.delete()
        return Response({"success": True})

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class FriendViewSet(viewsets.ModelViewSet):
    """
    Viewset to list friends, remove friends, add or remove close friends
    """

    permission_classes = [IsAuthenticated, FriendOwnerPermission]
    serializer_class = FriendSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return []
        return Friend.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=["PUT"], url_path="close-friend/add")
    def add_close_friend(self, request, pk=None):
        friendship = Friend.objects.get(id=pk)
        self.check_object_permissions(request, friendship)

        if not friendship.is_close_friend:
            friendship.is_close_friend = True
            friendship.save()

        return Response({"success": True}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PUT"], url_path="close-friend/remove")
    def remove_close_friend(self, request, pk=None):
        friendship = Friend.objects.get(id=pk)
        self.check_object_permissions(request, friendship)

        if friendship.is_close_friend:
            friendship.is_close_friend = False
            friendship.save()

        return Response({"success": True}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["DELETE"], url_path="remove")
    def remove_friend(self, request, pk=None):
        friendship = Friend.objects.get(id=pk)
        self.check_object_permissions(request, friendship)

        with transaction.atomic():
            FriendRequest.objects.filter(
                from_user=friendship.user, to_user=friendship.friend
            ).delete()
            friendship.delete()

        return Response({"success": True}, status=status.HTTP_200_OK)
