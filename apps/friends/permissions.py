from rest_framework.permissions import BasePermission


class FriendRequestOwnerPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Checks that the logged in user has only access to thier friend requests
        """
        return request.user == obj.to_user


class FriendOwnerPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Checks that the logged in user has only access to thier friend requests
        """
        return request.user == obj.user
