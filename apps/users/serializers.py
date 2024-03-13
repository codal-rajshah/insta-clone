import re
from rest_framework import serializers

from apps.users.models import UserProfile, User


class UserProfileSerializer(serializers.ModelSerializer):
    """
    UserProfile model serializer
    """

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "name",
            "mobile_number",
            "bio",
            "date_of_birth",
            "account_type",
        ]
        read_only_fields = ["profile_image"]

    def validate_mobile_number(self, mobile_number):
        regular_exp = "[6-9][0-9]{9}"
        pattern = re.compile(regular_exp)
        if re.match(pattern, mobile_number) is None:
            raise serializers.ValidationError(
                "Please enter 10 digit mobile number!"
            )
        return mobile_number


class UserSerializer(serializers.ModelSerializer):
    """
    ModelSeializer for user creation
    """

    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ["id", "email", "username", "profile"]
