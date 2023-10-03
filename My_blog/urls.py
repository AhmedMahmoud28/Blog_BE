from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication

from My_blog.swagger import CustomOpenAPISchemaGenerator

# Admin settings
admin.site.site_header = "My_blog"
admin.site.site_title = "My_blog site admin"
admin.site.index_title = "My_blog site administration"

# URL settings

main_patterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("api/", include("My_blog.userapp.urls")),
    path("api/", include("My_blog.blogapp.urls")),
)
urlpatterns = main_patterns


# Health url
urlpatterns += [
    path("health/", lambda res: HttpResponse("good")),
    path("silk/", include("silk.urls", namespace="silk")),
]


# swagger urls and configuration
schema_view = get_schema_view(
    openapi.Info(
        title="My_blog API",
        default_version="v1",
        description="My_blog Swagger Documentation",
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
    authentication_classes=(SessionAuthentication,),
    generator_class=CustomOpenAPISchemaGenerator,
    patterns=main_patterns,
)
urlpatterns += [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
