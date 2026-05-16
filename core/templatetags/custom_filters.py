from django import template

register = template.Library()

@register.filter(name='times')
def times(number):
    try:
        return range(int(number))
    except Exception:
        return []

@register.filter(name='get_item')
def get_item(obj, key):
    try:
        # Try integer index first (for lists)
        return obj[int(key)]
    except (ValueError, TypeError):
        # If not an integer, treat as dictionary key
        try:
            return obj[key]
        except Exception:
            return None
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
@register.filter(name='dict_lookup')
def dict_lookup(dictionary, key):
    """Retrieve value from dict using a key"""
    if isinstance(dictionary, dict):
        return dictionary.get(key, '')
    return ''