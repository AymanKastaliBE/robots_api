# gdrfad_api/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def sum_clicks(list_of_dicts):
    total_clicks = sum(item.get('click', 0) for item in list_of_dicts)
    return total_clicks