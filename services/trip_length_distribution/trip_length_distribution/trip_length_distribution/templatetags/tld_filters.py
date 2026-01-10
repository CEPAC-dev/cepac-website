import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def times(n):
    try:
        n = int(n)
    except Exception:
        return []
    return range(n)

@register.filter
def index(seq, i):
    try:
        return seq[int(i)]
    except Exception:
        return ""

@register.filter
def get_item(seq, i):
    try:
        return seq[int(i)]
    except Exception:
        return ""

@register.filter
def multiply(v, m):
    try:
        return float(v) * float(m)
    except Exception:
        return 0

@register.filter
def tojson(value):
    return mark_safe(json.dumps(value))
