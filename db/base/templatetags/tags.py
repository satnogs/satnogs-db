from django import template
from django.core.urlresolvers import reverse
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def active(request, urls):
    if request.path in (reverse(url) for url in urls.split()):
        return 'active'
    return None


@register.filter
def frq(value):
    try:
        to_format = float(value)
    except (TypeError, ValueError):
        return ''
    prec = to_format / 1000
    formatted = format(to_format / 1000000, '.3f')
    if not prec.is_integer():
        point = str(prec - int(prec))[2:]
        formatted = format_html('{0}<small>{1}</small> MHz', formatted, point)
    return formatted
