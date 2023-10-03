from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, StackedInline

from My_blog.userapp import models


class AddressInline(StackedInline):
    model = models.Address
    min_num = 0
    extra = 0
    classes = ["collapse"]


@admin.register(models.User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = [
        "id",
        "email",
        "first_name",
        "last_name",
    ]
    inlines = [AddressInline]
    fieldsets = (
        (
            None,
            {"fields": ("username", "password", "phone", "is_development_api_user")},
        ),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


""" Address """


@admin.register(models.Address)
class AddressAdmin(ModelAdmin):
    list_display = ["id", "user", "country", "region", "postal_code", "description"]
    list_select_related = ("country", "region", "user")
    autocomplete_fields = ["user", "country"]
    search_fields = (
        "user__email",
        "user__username",
        "country__name",
        "region__name",
        "description",
    )


""" Notification """


@admin.register(models.Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ["id", "user", "title", "text", "seen", "date_time"]
    list_select_related = ("user",)
    search_fields = ("user__email",)
    autocomplete_fields = ["user"]
