from rest_framework import permissions


class UserViewPermission(permissions.BasePermission):
    """
    used only in one view (UserView):
    """

    def has_permission(self, request, view):
        if request.method in ["PUT", "GET", "PATCH", "OPTIONS"]:
            return bool(request.user and request.user.is_authenticated)
        elif request.method == "POST":
            return True
        return False
