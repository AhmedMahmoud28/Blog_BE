{%  load code_generator_tags %}
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

{% from_module_import app.name|add:'.models' models %}
{% from_module_import app.name|add:'.serializers' models|add_to_items:'Serializer' %}
{% from_module_import app.name|add:'.filters' models|add_to_items:'Filter' %}


{% for model in models %}
class {{ model.name }}ViewSet(viewsets.ModelViewSet):
    queryset = {{ model.name }}.objects.all()
    serializer_class = {{ model.name }}Serializer
    permission_classes = (IsAuthenticated,)
    search_fields = (
        {% indent_items model.string_field_names 8 quote='simple' %}
    )
    filterset_class = {{ model.name }}Filter
    ordering_fields = (
        {% indent_items model.concrete_field_names 8 quote='simple' %}
    )
{% endfor %}
