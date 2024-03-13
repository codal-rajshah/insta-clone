from django.urls import path, include


urlpatterns = [path("v1/", include("apps.posts.v1.urls"))]
