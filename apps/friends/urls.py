from django.urls import path, include


urlpatterns = [path("v1/", include("apps.friends.v1.urls"))]
