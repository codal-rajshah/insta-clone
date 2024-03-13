from django.contrib import admin

from apps.posts.models import Post, PostLike, PostComment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "caption",
        "file",
        "hide_like_and_view_counts",
        "turn_off_comments",
        "audience",
    ]


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ["post", "liked_by", "is_liked"]


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ["post", "commented_by", "comment"]
