{%  load code_generator_tags %}
from django_filters import rest_framework as filters

{% from_module_import app.name|add:'.models' models %}


{% for model in models %}
class {{ model.name }}Filter(filters.FilterSet):
    class Meta:
        model = {{ model.name }}
        fields = [{% indent_items model.field_names 12 quote='simple' %}]
{% endfor %}
