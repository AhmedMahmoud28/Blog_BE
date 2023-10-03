import pytest
from django.core import mail
from django.urls import reverse

pytestmark = pytest.mark.django_db
lazy_fixture = pytest.lazy_fixture


class TestUserView:
    @pytest.mark.parametrize(
        "data",
        [
            lazy_fixture("user_sign_up_data"),
        ],
    )
    def test_sign_up(self, api_client, data):
        url = reverse("me")
        resp = api_client.post(url, data)
        print(resp.json())
        assert resp.status_code == 201


class TestAddress:
    @pytest.mark.parametrize(
        "url_resolver,client,status",
        [
            (
                "addresses-list",
                lazy_fixture("api_client"),
                401,
            ),
            (
                "addresses-list",
                lazy_fixture("api_client_with_credentials"),
                200,
            ),
        ],
    )
    def test_list_addresses(self, url_resolver, client, status):
        url = reverse(url_resolver)
        resp = client.get(url)
        assert resp.status_code == status

    @pytest.mark.parametrize(
        "url_resolver,client,status,instance,assign_different_user",
        [
            (
                "addresses-detail",
                lazy_fixture("api_client"),
                401,
                lazy_fixture("address"),
                False,
            ),
            (
                "addresses-detail",
                lazy_fixture("api_client_with_credentials"),
                404,
                lazy_fixture("address"),
                True,
            ),
            (
                "addresses-detail",
                lazy_fixture("api_client_with_credentials"),
                200,
                lazy_fixture("address"),
                False,
            ),
        ],
    )
    def test_get_address(
        self,
        url_resolver,
        client,
        status,
        user_factory,
        instance,
        assign_different_user,
    ):
        if assign_different_user:
            instance.user = user_factory.create()
            instance.save()
        url = reverse(url_resolver, kwargs={"pk": instance.id})
        resp = client.get(url)
        assert resp.status_code == status

    @pytest.mark.parametrize(
        "url_resolver,data,client,status",
        [
            (
                "addresses-list",
                lazy_fixture("address_data"),
                lazy_fixture("api_client"),
                401,
            ),
            (
                "addresses-list",
                lazy_fixture("address_data"),
                lazy_fixture("api_client_with_credentials"),
                201,
            ),
        ],
    )
    def test_create_address(self, url_resolver, data, client, status, user):
        url = reverse(url_resolver)
        resp = client.post(url, data)
        assert resp.status_code == status
        resp_data = resp.json()
        if status == 201:
            assert resp_data.get("id") == user.address_set.last().id

    @pytest.mark.parametrize(
        "url_resolver,data,instance,client,status",
        [
            (
                "addresses-detail",
                lazy_fixture("address_data"),
                lazy_fixture("address"),
                lazy_fixture("api_client"),
                401,
            ),
            (
                "addresses-detail",
                lazy_fixture("address_data"),
                lazy_fixture("address"),
                lazy_fixture("api_client_with_credentials"),
                200,
            ),
        ],
    )
    def test_update_address(self, url_resolver, data, instance, client, status, user):
        url = reverse(url_resolver, kwargs={"pk": instance.id})
        resp = client.put(url, data)
        assert resp.status_code == status

    @pytest.mark.parametrize(
        "url_resolver,instance,client,status",
        [
            (
                "addresses-detail",
                lazy_fixture("address"),
                lazy_fixture("api_client"),
                401,
            ),
            (
                "addresses-detail",
                lazy_fixture("address"),
                lazy_fixture("api_client_with_credentials"),
                405,
            ),
        ],
    )
    def test_delete_address(self, url_resolver, instance, client, status, user):
        url = reverse(url_resolver, kwargs={"pk": instance.id})
        resp = client.delete(url)
        assert resp.status_code == status
