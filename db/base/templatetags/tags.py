from django import template
from django.core.urlresolvers import reverse

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
    if to_format % 1000 == 0:
        formatted = format(float(to_format) / 1000000, '.3f')
    else:
        formatted = format(float(to_format) / 1000000, '.6f')
    formatted = formatted + ' Mhz'
    return formatted
