from rest_framework import permissions

# is_development_api_user


class DevelopmentAPIUserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_development_api_user)
