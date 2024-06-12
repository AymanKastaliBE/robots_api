from django import template

register = template.Library()

@register.filter(name='user_in_group')
def user_in_group(user, group_names):
    groups = group_names.split(',')
    return user.groups.filter(name__in=groups).exists()