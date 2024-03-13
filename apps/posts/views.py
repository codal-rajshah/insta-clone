from rest_framework import viewsets
from rest_framework import status
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import mixins

from django.db.models import Q, Subquery
from django.core.cache import cache

from apps.common.pagination import StandardResultsSetPagination
from apps.friends.models import Friend
from apps.common.utils import set_json_renderer
from apps.posts.permissions import MustBeFriendPermission
from apps.posts.forms import PostLikeForm

from apps.posts.serializers import (
    FeedSerializer,
    PostDetailSerializer,
    PostSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    PostCommentCreateSerializer,
)
from apps.posts.models import Post, PostLike


class PostViewSet(viewsets.ModelViewSet):
    """ """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return []
        return (
            Post.objects.filter(user=self.request.user)
            .select_related("user", "user__profile")
            .order_by("-created")
        )

    def get_serializer_class(self):
        if self.action == "upload_file":
            return PostCreateSerializer
        elif self.action == "update":
            return PostUpdateSerializer
        elif self.action == "retrieve":
            return PostDetailSerializer
        return self.serializer_class

    @action(
        detail=False,
        methods=["POST"],
        url_path="upload/file",
        parser_classes=[FileUploadParser],
    )
    def upload_file(self, request):
        user = request.user
        file = request.data["file"]

        new_post = Post(user=user)
        new_post.file = file
        new_post.save()

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=new_post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class FeedViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        posts = (
            Post.objects.filter(
                Q(
                    audience="friends",
                    user__in=Subquery(
                        Friend.objects.filter(user=user).values_list(
                            "friend", flat=True
                        )
                    ),
                ) | Q(audience="close_friends", user__friends__is_close_friend=True)
            )
            .select_related("user", "user__profile")
            .order_by("-updated")
            .distinct()
        )
        return posts

    def list(self, request, *args, **kwargs):
        cache_key = f"{request.user.id}_posts_feed"
        response = cache.get(cache_key)

        if response is not None:
            return response

        response = super().list(request, *args, **kwargs)
        response = set_json_renderer(response)
        cache.set(cache_key, response.render(), 60 * 3)
        return response


# class PostLikeViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
#     serializer_class = PostLikeCreateSerializer
#     permission_classes = [IsAuthenticated, MustBeFriendPermission]

#     def like(self, request, *args, **kwargs):
#         data = request.data
#         data["liked_by"] = request.user.id
#         serializer = self.serializer_class(data=request.data)

#         if serializer.is_valid():
#             post = serializer.validated_data["post"]
#             self.check_object_permissions(request, post)
#             serializer.save()
#             return Response({"success": True}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostLikeAPIView(views.APIView):
    permission_classes = [IsAuthenticated, MustBeFriendPermission]

    def post(self, request):
        data = request.data
        form = PostLikeForm(data=data)
        if form.is_valid():
            post = form.cleaned_data.get("post")
            self.check_object_permissions(request, post)

            action = form.cleaned_data.get("action")
            post_like, _ = PostLike.objects.get_or_create(
                liked_by=request.user,
                post=post
            )

            if action == 'like':
                post_like.is_liked = True
            else:
                post_like.is_liked = False
            post_like.save()
            return Response({"success": True}, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class PostCommentViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = PostCommentCreateSerializer
    permission_classes = [IsAuthenticated, MustBeFriendPermission]

    def create(self, request, *args, **kwargs):
        data = request.data
        data._mutable = True
        data["commented_by"] = request.user.id
        data._mutable = False
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            post = serializer.validated_data["post"]
            self.check_object_permissions(request, post)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
