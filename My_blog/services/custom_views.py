from My_blog.services.exceptions import Http400


class QueryParamsValidatoer(object):
    def initial(self, *args, **kwargs):
        if not hasattr(self, "required_query_params"):
            return super(QueryParamsValidatoer, self).initial(*args, **kwargs)
        for field in self.required_query_params:
            if not self.request.query_params.get(field):
                raise Http400(
                    {"details": ["field %s is required in query params" % (field)]}
                )
        return super(QueryParamsValidatoer, self).initial(*args, **kwargs)


class UserFilterMixin(object):
    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user.id)
