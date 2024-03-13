import factory
from factory.django import DjangoModelFactory

from apps.posts.models import Post, PostLike, PostComment


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    file = factory.django.FileField()


class PostLikeFactory(DjangoModelFactory):
    class Meta:
        model = PostLike


class PostCommentFactory(DjangoModelFactory):
    class Meta:
        model = PostComment
