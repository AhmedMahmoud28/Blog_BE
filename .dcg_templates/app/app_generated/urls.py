{%  load code_generator_tags %}
from django.urls import include, path
from rest_framework import routers

{% from_module_import app.name|add:'.views' models|add_to_items:'ViewSet' %}


router = routers.DefaultRouter()
{% for model in models %}
router.register('{{ model.snake_case_name }}s', {{ model }}ViewSet)
{%endfor%}

urlpatterns = [
    path('', include(router.urls)),
]
