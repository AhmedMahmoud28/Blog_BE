from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BlogappConfig(AppConfig):
    name = "My_blog.blogapp"
    verbose_name = _("Blog App")
