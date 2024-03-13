from factory.django import DjangoModelFactory

from apps.friends.models import Friend, FriendRequest


class FriendRequestFactory(DjangoModelFactory):
    class Meta:
        model = FriendRequest


class FriendFactory(DjangoModelFactory):
    class Meta:
        model = Friend
