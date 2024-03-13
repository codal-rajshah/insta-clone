from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin.sites import NotRegistered
from apps.users.models import UserProfile

User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "User profile"


class UserAdmin(BaseUserAdmin):
    """
    Admin interface for the User model.
    """

    inlines = (UserProfileInline,)


# Unregister the default UserAdmin
try:
    admin.site.unregister(User)
except NotRegistered:
    pass

# Register our UserAdmin
admin.site.register(User, UserAdmin)
