from django.template import Library
from apps.main.models import CategoryModel

register = Library()

@register.simple_tag()
def get_categories():
    return CategoryModel.objects.all