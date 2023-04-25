from django import template
from apps.blog.models import Category

register = template.Library()


@register.inclusion_tag('_heading.html')
def show_menu(heading_class='heading'):
    categories = Category.objects.all()
    return {'categories': categories, 'heading_class': heading_class}