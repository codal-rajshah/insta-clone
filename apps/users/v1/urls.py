from django.urls import path
from rest_framework import routers

from apps.users import views

default_router = routers.DefaultRouter()

default_router.register(r"", views.UserViewSet)

urlpatterns = [
    path("create", views.UserCreationView.as_view(), name="user-creation"),
    path("create/<int:pk>/", views.UserCreationView.as_view(), name="user-detail"),
]

urlpatterns += default_router.urls
