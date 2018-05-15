from django import template

register = template.Library()

@register.filter()
def another_filter(value_1, value_2):
    return value_1, value_2

@register.filter()
def custom_filter(another_filter_value, tab):
    value_1, value_2 = another_filter_value

    return tab[value_1][value_2]