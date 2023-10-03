{%  load code_generator_tags %}
from import_export import resources
{% from_module_import app.name|add:'.models' models %}


{% for model in models %}
class {{ model.name }}Resource(resources.ModelResource):
    class Meta:
        model = {{ model.name }}
        fields = [{% indent_items model.filter_field_names 8 quote='simple' %}]
        export_order = fields
{% endfor %}
