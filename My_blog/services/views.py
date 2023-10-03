from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.settings import api_settings


class ModelViewSetClones:
    """
    Create a model instance.
    """

    def create_clone(self, request, data=True, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if data:
            self.perform_create(serializer)
            data = serializer.data
        else:
            data = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    """
    List a queryset.
    """

    def list_clone(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    """
    Retrieve a model instance.
    """

    def retrieve_clone(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    """
    Update a model instance.
    """

    def update_clone(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    """
    Destroy a model instance.
    """

    def destroy_clone(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class BulkCreateModelMixin(mixins.CreateModelMixin):
    def get_serializer(self, *args, **kwargs):
        if self.action == "create":
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)


class GenericCreateModelMixin(mixins.CreateModelMixin):
    def get_serializer(self, *args, **kwargs):
        if type(kwargs.get("data", {})) == list:
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)
