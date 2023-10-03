from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey

from My_blog.services.custom_Models import CustomModel
from My_blog.services.helpers import rand_int_4digits
from My_blog.userapp.conf import OFFER, VISIT
from My_blog.userapp.model_mixins import UserMixin


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields["is_active"] = True
        return super().create_superuser(username, email, password, **extra_fields)


class User(UserMixin, CustomModel, AbstractUser):
    email = models.EmailField(
        verbose_name="email address",
        unique=True,
    )
    username = models.CharField(
        _("username"),
        max_length=150,
    )
    phone = models.CharField(_("Phone"), max_length=50, null=True, blank=True)

    # verification
    is_active = models.BooleanField(default=False)

    verification_code = models.CharField(
        max_length=10, default=rand_int_4digits, null=True, blank=True
    )
    is_deleted = models.BooleanField(default=False)
    is_development_api_user = models.BooleanField(
        default=False,
        help_text=_(
            "indicate if this user could be used in developer "
            "only private APIs like create statistics endpoints."
        ),
    )
    password_reset_code = models.CharField(max_length=10, null=True, blank=True)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


# Address


class Address(models.Model):
    user = models.ForeignKey("User", verbose_name=_("User"), on_delete=models.CASCADE)
    country = models.ForeignKey(
        "cities_light.Country",
        verbose_name=_("Country"),
        on_delete=models.SET_NULL,
        null=True,
    )
    region = ChainedForeignKey(
        "cities_light.Region",
        verbose_name=_("Region"),
        on_delete=models.SET_NULL,
        null=True,
        chained_field="country",
        chained_model_field="country",
        show_all=False,
        auto_choose=True,
    )
    description = models.TextField(_("Description"))
    postal_code = models.CharField(_("Postal code"), max_length=100)
    is_default = models.BooleanField(_("Is default"), default=False)

    def __str__(self) -> str:
        return f"{self.country}, {self.region}, {self.description}"

    class Meta:
        verbose_name_plural = "Addresses"


# Notifications


class Notification(models.Model):
    user = models.ForeignKey("User", verbose_name=_("User"), on_delete=models.CASCADE)
    title = models.TextField(_("Title"))
    text = models.TextField(_("Text"))
    seen = models.BooleanField(_("Seen"), default=False)
    date_time = models.DateTimeField(_("Date Time"), auto_now=False, auto_now_add=True)

    # models related
    NOTIFICATION_MODELS = (
        (VISIT, _("Visit")),
        (OFFER, _("Offer")),
    )
    model = models.CharField(
        _("Notification Model"), max_length=50, choices=NOTIFICATION_MODELS
    )
    model_id = models.IntegerField(_("Model ID"))
