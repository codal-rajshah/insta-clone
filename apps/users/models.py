from django.db import models
from django.contrib.auth import get_user_model

from apps.common.models import TimeStampedModel

User = get_user_model()


class UserProfile(TimeStampedModel):
    """
    Model to manage profile of particular user
    """

    ACCOUNT_TYPE_CHOICES = [
        ("private", "Private"),
        ("public", "Public"),
        ("professional", "Professional"),
    ]

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    mobile_number = models.CharField(max_length=10, db_index=True)
    profile_image = models.FileField(upload_to="profile_images/")
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField()

    account_type = models.CharField(
        max_length=50, choices=ACCOUNT_TYPE_CHOICES, default="public"
    )


class UserLink(TimeStampedModel):
    """
    External links added by users
    """

    user = models.ForeignKey(User, related_name="links", on_delete=models.CASCADE)
    link = models.URLField()
    title = models.CharField(max_length=50, db_index=True)
