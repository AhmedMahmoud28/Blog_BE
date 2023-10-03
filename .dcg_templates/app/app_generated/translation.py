{%  load code_generator_tags %}
from modeltranslation.translator import register, TranslationOptions
{% from_module_import app.name|add:'.models' models %}


{% for model in models %}
@register({{ model.name }})
class {{ model.name }}TranslationOptions(TranslationOptions):
    fields = [{% indent_items model.filter_field_names 8 quote='simple' %}]
{% endfor %}
