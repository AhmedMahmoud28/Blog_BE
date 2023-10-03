from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from My_blog.services.views import ModelViewSetClones
from My_blog.userapp import models
from My_blog.userapp.permissions import UserViewPermission
from My_blog.userapp.serializers import (
    LoginSerializer,
    UserDataSerializer,
    UserSerializer,
)


class UserViewSet(ModelViewSetClones, viewsets.GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserViewPermission]

    def get_serializer_class(self):
        if self.action == "login":
            return LoginSerializer
        elif self.action == "update_me":
            return UserDataSerializer
        elif self.action == "get_me":
            return UserDataSerializer
        return super().get_serializer_class()

    @action(methods=["post"], detail=False)
    def register(self, request, *args, **kwargs):
        return super().create_clone(request, *args, **kwargs)

    @action(methods=["post"], detail=False)
    def login(self, request, *args, **kwargs):
        return super().create_clone(request, data=False, *args, **kwargs)

    @action(methods=["get"], detail=False)
    def get_me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(methods=["put"], detail=False)
    def update_me(self, request):
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=["delete"], detail=False)
    def delete_me(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
