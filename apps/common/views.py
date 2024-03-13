from datetime import timedelta
import uuid

from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from oauth2_provider.models import Application, AccessToken

from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@api_view(["POST"])
@throttle_classes([AnonRateThrottle])
def create_access_token(request):
    client_id = request.data.get("client_id")
    client_secret = request.data.get("client_secret")
    username = request.data.get("username")
    password = request.data.get("password")

    try:
        application = Application.objects.get(
            client_id=client_id, client_secret=client_secret
        )
    except Application.DoesNotExist:
        return Response({"error": "Invalid client credentials"}, status=400)

    user = User.objects.filter(username=username).first()
    if not user or not user.check_password(password):
        return Response({"error": "Invalid username or password"}, status=400)

    expires = timezone.now() + timedelta(hours=24)
    access_token = AccessToken.objects.create(
        user=user,
        application=application,
        expires=expires,
        token=uuid.uuid4().hex,
    )

    return Response({"access_token": access_token.token})
