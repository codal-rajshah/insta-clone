from django.contrib import admin

from apps.friends.models import Friend, FriendRequest


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ["from_user", "to_user", "accepted"]


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ["user", "friend", "is_close_friend"]
