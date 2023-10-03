from .base import *  # noqa
from .base import config

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = config("DJANGO_SECRET_KEY", cast=str)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]

# DATABASES
# ------------------------------------------------------------------------------
# DATABASES["default"] = config("DATABASE_URL", cast=str)
DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa
DATABASES["default"]["CONN_MAX_AGE"] = config(  # noqa
    "CONN_MAX_AGE", default=60, cast=int
)  # noqa F405

# CACHES
# ------------------------------------------------------------------------------
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": config("REDIS_URL", cast=str),
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             # Mimicing memcache behavior.
#             # https://github.com/jazzband/django-redis#memcached-exceptions-behavior
#             "IGNORE_EXCEPTIONS": True,
#         },
#     }
# }

# SECURITY
# ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# # https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
# SECURE_SSL_REDIRECT = config("DJANGO_SECURE_SSL_REDIRECT", default=True, cast=bool)
# # https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
# SESSION_COOKIE_SECURE = True
# # https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
# CSRF_COOKIE_SECURE = True
# # https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# # TODO: set this to 60 seconds first and then to 518400 once you prove the former works # noqa
# SECURE_HSTS_SECONDS = 60
# # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains # noqa
# SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
#     "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True, cast=bool
# )
# # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
# SECURE_HSTS_PRELOAD = config("DJANGO_SECURE_HSTS_PRELOAD", default=True, cast=bool)
# # https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
# SECURE_CONTENT_TYPE_NOSNIFF = config(
#     "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True, cast=bool
# )

# AWS related stuff
AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
    "Expires": "Thu, 31 Dec 2099 20:00:00 GMT",
    "Cache-Control": "max-age=94608000",
}

DEFAULT_FILE_STORAGE = "My_blog.s3utils.MediaS3BotoStorage"
STATICFILES_STORAGE = "My_blog.s3utils.StaticS3BotoStorage"

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", cast=str)
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", cast=str)
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default=False, cast=str)
AWS_S3_HOST = "s3.%s.amazonaws.com" % config(
    "AWS_STORAGE_BUCKET_REGION", default=False, cast=str
)
S3_URL = "http://%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
STATIC_DIRECTORY = "/My_blog/static/"
MEDIA_DIRECTORY = "/My_blog/media/"

# Email
EMAIL_BACKEND = config("EMAIL_BACKEND")
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_USE_TLS = config("EMAIL_USE_TLS")
EMAIL_PORT = config("EMAIL_PORT")
SERVER_EMAIL = config("SERVER_EMAIL")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

# Your stuff...
# ------------------------------------------------------------------------------
