from django import template

register = template.Library()


@register.filter
def calculate_total_amount(value, arg):
    try:
        return value + arg
    except (TypeError, ValueError):
        return ''