from django.urls import path
from apps.common import views

urlpatterns = [
    path(
        "oauth2/access_token",
        views.create_access_token,
        name="create-access-token",
    )
]
