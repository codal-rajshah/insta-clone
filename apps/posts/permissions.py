from rest_framework.permissions import BasePermission

from django.db.models import Q

from apps.friends.models import Friend


class MustBeFriendPermission(BasePermission):
    """
    Must be friend to perform certain actions
    """

    def has_object_permission(self, request, view, post):
        post_owner = post.user
        requested_user = request.user

        if post.audience == "close_friends":
            return Friend.objects.filter(
                user=post_owner, friend=requested_user, is_close_friend=True
            ).exists()
        else:
            filters = Q(user=requested_user) & Q(friend=post_owner)
            return Friend.objects.filter(filters).exists()
