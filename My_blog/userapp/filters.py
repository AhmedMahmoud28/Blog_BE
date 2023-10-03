from django_filters import rest_framework as filters

from My_blog.userapp.models import Notification, User


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ["id", "email"]


class NotificationFilter(filters.FilterSet):
    """"""

    class Meta:
        model = Notification
        fields = ["model", "model_id"]
