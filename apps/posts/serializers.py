from rest_framework import serializers

from django.contrib.auth import get_user_model

from apps.posts.models import Post, PostComment, PostLike

User = get_user_model()


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Serializer to create post
    """

    class Meta:
        model = Post
        fields = ["id"]


class PostUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer to update post
    """

    class Meta:
        model = Post
        fields = [
            "caption",
            "location",
            "music",
            "hide_like_and_view_counts",
            "turn_off_comments",
            "audience",
        ]


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer to send the JSON response
    """

    class Meta:
        model = Post
        fields = [
            "id",
            "file",
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    """
    Serializer to send the JSON response
    """

    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.get_likes_count()

    def get_comments_count(self, obj):
        return obj.get_comments_count()

    def get_likes(self, obj):
        likes = obj.likes.filter(is_liked=True).order_by("-updated")
        return PostLikeSerializer(likes, many=True).data

    def get_comments(self, obj):
        comments = obj.comments.all().order_by("-updated")
        return PostCommentSerializer(comments, many=True).data

    class Meta:
        model = Post
        fields = [
            "caption",
            "location",
            "music",
            "hide_like_and_view_counts",
            "turn_off_comments",
            "audience",
            "user",
            "file",
            "likes_count",
            "comments_count",
            "likes",
            "comments",
            "id",
        ]


class PostLikeSerializer(serializers.ModelSerializer):
    """
    Serializes post likes for JSON response
    """

    username = serializers.CharField(source="liked_by.username")
    user_id = serializers.IntegerField(source="liked_by.id")
    profile_picture = serializers.SerializerMethodField()

    def get_profile_picture(self, post):
        try:
            return post.liked_by.profile.profile_image.url
        except ValueError:
            return None

    class Meta:
        model = PostLike
        fields = ("username", "user_id", "profile_picture")


class PostCommentSerializer(serializers.ModelSerializer):
    """
    Serializes post comments for JSON Response
    """

    username = serializers.CharField(source="commented_by.username")
    user_id = serializers.IntegerField(source="commented_by.id")
    profile_picture = serializers.SerializerMethodField()

    def get_profile_picture(self, post):
        try:
            return post.commented_by.profile.profile_image.url
        except ValueError:
            return None

    class Meta:
        model = PostComment
        fields = ("username", "user_id", "profile_picture", "comment")


class FeedSerializer(PostDetailSerializer):
    """
    Serializer to send the JSON response for feed of friends
    """

    def get_likes_count(self, obj):
        if obj.hide_like_and_view_counts:
            return None
        return super().get_likes_count(obj)

    def get_comments_count(self, obj):
        if obj.turn_off_comments:
            return None
        return super().get_comments_count(obj)


class PostLikeCreateSerializer(serializers.ModelSerializer):
    """
    Serializer to create post like object
    """
    class Meta:
        model = PostLike
        fields = ["post", "liked_by", "is_liked"]


class PostCommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer to create post comment object
    """

    class Meta:
        model = PostComment
        fields = ["post", "commented_by", "comment"]
