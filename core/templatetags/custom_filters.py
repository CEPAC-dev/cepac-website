from django import template

register = template.Library()

@register.filter(name='times')
def times(number):
    try:
        return range(int(number))
    except Exception:
        return []

@register.filter(name='get_item')
def get_item(lst, index):
    try:
        return lst[int(index)]
    except Exception:
        return None

@register.filter(name='next_or_end')
def next_or_end(value, arg):
    try:
        index = list(arg).index(value)
        return arg[index + 1] if index + 1 < len(arg) else "End"
    except Exception:
        return "End"

@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except Exception:
        try:
            return value * arg
        except Exception:
            return value
