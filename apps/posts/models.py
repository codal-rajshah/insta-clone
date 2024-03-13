from django.db import models
from django.contrib.auth import get_user_model

from apps.common.models import TimeStampedModel

User = get_user_model()


class Post(TimeStampedModel):
    """
    Model to save the post in database
    """

    AUDIENCE_CHOICES = (
        ("friends", "Friends"),
        ("close_friends", "Close Friends"),
    )
    user = models.ForeignKey(
        User, related_name="posts", on_delete=models.CASCADE
    )

    # post related fields
    file = models.FileField(upload_to="posts/")
    caption = models.CharField(max_length=300, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    music = models.CharField(max_length=50, null=True, blank=True)
    hide_like_and_view_counts = models.BooleanField(default=False)
    turn_off_comments = models.BooleanField(default=False)
    audience = models.CharField(
        max_length=20, choices=AUDIENCE_CHOICES, default="friends"
    )

    def __str__(self):
        return f"{self.id} : {self.user.username} - {self.audience}"

    def get_likes_count(self):
        return self.likes.filter(is_liked=True).count()

    def get_comments_count(self):
        return self.comments.count()


class PostLike(TimeStampedModel):
    """
    Model to save post likes
    """

    post = models.ForeignKey(
        Post, related_name="likes", on_delete=models.CASCADE
    )
    liked_by = models.ForeignKey(
        User, related_name="user_likes", on_delete=models.CASCADE
    )
    is_liked = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.post.id} - {self.liked_by}"

    class Meta:
        unique_together = ("post", "liked_by")


class PostComment(TimeStampedModel):
    """
    Model to save post comments
    """

    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE
    )
    commented_by = models.ForeignKey(
        User, related_name="user_comments", on_delete=models.CASCADE
    )
    comment = models.TextField()
