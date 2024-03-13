
import factory
from factory.django import DjangoModelFactory
from datetime import timedelta
from oauth2_provider.models import Application, AccessToken

from django.utils import timezone

from apps.users.models import User
from apps.common.utils import uuid_hex


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('email', 'username')

    _DEFAULT_PASSWORD = 'Password@1234'

    username = factory.Sequence('test{}'.format)
    email = factory.Sequence('test{}@codal.com'.format)
    password = factory.PostGenerationMethodCall('set_password', _DEFAULT_PASSWORD)
    is_staff = False
    is_active = True
    is_superuser = False


class ApplicationFactory(DjangoModelFactory):
    class Meta:
        model = Application

    client_id = factory.LazyFunction(uuid_hex)
    client_secret = factory.LazyFunction(uuid_hex)
    authorization_grant_type = 'authorization-code'
    name = 'test'
    client_type = 'public'


class AccessTokenFactory(DjangoModelFactory):
    class Meta:
        model = AccessToken

    user = None
    application = None
    expires = timezone.now() + timedelta(hours=24)
    token = factory.LazyFunction(uuid_hex)
