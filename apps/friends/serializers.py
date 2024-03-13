from rest_framework import serializers
from django.contrib.auth.models import User
from apps.friends.models import FriendRequest, Friend
from apps.users.serializers import UserSerializer


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Friend request serializer
    """

    to_user = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="username"
    )

    class Meta:
        model = FriendRequest
        fields = ["to_user"]

    def create(self, validated_data):
        to_user = validated_data.get("to_user")
        from_user = self.context["request"].user

        if to_user == from_user:
            raise serializers.ValidationError(
                {"detail": "You cannot add yourself as friend"}
            )

        friend_request = self.Meta.model.objects.create(
            from_user=from_user, to_user=to_user
        )
        friend_request.save()
        return friend_request


class FriendRequestResponseSerializer(serializers.ModelSerializer):
    """
    Will be used to serialize the response
    """

    friend_request = UserSerializer(read_only=True, source="from_user")
    request_id = serializers.IntegerField(source="id")

    class Meta:
        model = FriendRequest
        fields = ["friend_request", "request_id"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        nested_data = data.pop("friend_request")
        if nested_data:
            data.update(nested_data)
        return data


class FriendSerializer(serializers.ModelSerializer):
    """
    Will be used to serialize the response
    """

    friend = UserSerializer(read_only=True)
    friend_id = serializers.IntegerField(source="id")

    class Meta:
        model = Friend
        fields = ["friend", "friend_id", "is_close_friend"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        nested_data = data.pop("friend")
        if nested_data:
            data.update(nested_data)
        return data
