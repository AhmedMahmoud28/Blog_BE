import pytest
from rest_framework.authtoken.models import Token

from My_blog.addonsapp.factories import *  # noqa
from My_blog.userapp.tests.factories import *  # noqa
from My_blog.userapp.tests.factories import UserFactory  # noqa


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def get_or_create_token(db, user):
    token, _ = Token.objects.get_or_create(user=user)
    return token


@pytest.fixture
def api_client_with_credentials(db, user, api_client):
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
