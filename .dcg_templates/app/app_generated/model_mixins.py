{%  load code_generator_tags %}{% for model in models %}

""" {{ model.name }} Mixin """


class {{ model.name }}Mixin(object):
    pass
{% endfor %}
