import pytest


@pytest.fixture
def address_data(db, user, country, region):
    return {
        "country": country.id,
        "region": region.id,
        "description": "description test",
        "postal_code": "postal test",
        "is_default": False,
    }


@pytest.fixture
def user_sign_up_data(country):
    return {
        "email": "user@example.com",
        "username": "string",
        "phone": "string",
        "password": "string",
    }
