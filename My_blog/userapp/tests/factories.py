from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import Faker, post_generation
from factory.declarations import SubFactory
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from My_blog.addonsapp.factories import CountryFactory, RegionFactory
from My_blog.userapp.models import Address


@register
class UserFactory(DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).generate(params={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


@register
class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address

    user = SubFactory(UserFactory)
    country = SubFactory(CountryFactory)
    region = SubFactory(RegionFactory)
    description = Faker("text")
    postal_code = Faker("text", max_nb_chars=10)
