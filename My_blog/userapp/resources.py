from import_export import resources

from My_blog.userapp.models import Notification, User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = [
            "id",
            "password",
            "last_login",
            "first_name",
            "last_name",
            "date_joined",
            "email",
            "username",
            "phone",
            "verification_code",
            "password_reset_code",
        ]
        export_order = fields


class NotificationResource(resources.ModelResource):
    class Meta:
        model = Notification
        fields = ["id", "model", "model_id"]
        export_order = fields
