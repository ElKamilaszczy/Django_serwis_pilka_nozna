from django import template

register = template.Library()

@register.filter()
def another_filter(value_1, value_2):
    return value_1, value_2

@register.filter()
def custom_filter(another_filter_value, tab):
    value_1, value_2 = another_filter_value

    return tab[value_1][value_2]

#W celu iteracji tylko okresolna ilosc razy w szablonie
@register.filter(name='ile_razy')
def ile_razy(number):
    return range(1, number)

#W celu iteracji tylko okresolna ilosc razy w szablonie (na potrzeby kolejek)
@register.filter(name='ile_razy2')
def ile_razy2(number):
    return range(1, number+1)

@register.filter()
def first_filter(value_1, tab):
    return tab[value_1]
