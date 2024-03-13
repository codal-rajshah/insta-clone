from django.db import models
from django.contrib.auth import get_user_model
from apps.common.models import TimeStampedModel

User = get_user_model()


class FriendRequest(TimeStampedModel):
    """
    Friend requests from one user to another
    """

    from_user = models.ForeignKey(
        User, related_name="sent_request", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User, related_name="received_request", on_delete=models.CASCADE
    )
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("from_user", "to_user")


class Friend(TimeStampedModel):
    """
    Friends table to store the users after acceptance
    """

    user = models.ForeignKey(
        User, related_name="friends", on_delete=models.CASCADE
    )
    friend = models.ForeignKey(User, on_delete=models.CASCADE)
    is_close_friend = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "friend")
