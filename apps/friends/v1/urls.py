from rest_framework.routers import DefaultRouter

from apps.friends import views

default_router = DefaultRouter()

default_router.register("friends", views.FriendViewSet, basename="friends")
default_router.register("friend/request", views.FriendRequestViewSet)

urlpatterns = default_router.urls
