from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.inspectors import SwaggerAutoSchema


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    pass


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def determine_path_prefix(self, paths):
        return "/en/api/"
