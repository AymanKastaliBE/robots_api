from django import template

register = template.Library()


@register.filter
def calculate_total_amount(value, arg):
    try:
        return value + arg
    except (TypeError, ValueError):
        return ''
    

@register.filter
def calculate_filtered_amount_vat(bills):
    total = sum(bill.amount + bill.vat for bill in bills)
    return total