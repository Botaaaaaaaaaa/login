from django import template

register = template.Library()

@register.filter(name = 'inverse')
def inverse(value):
    return value[::-1]