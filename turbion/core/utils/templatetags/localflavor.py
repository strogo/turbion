from django import template
from django.conf import settings

register = template.Library()

@register.filter
def pluralize_rus(value, suf):
    suf = suf.split(',')
    if value == 0:
        return suf[0]
    elif value == 1:
        return suf[1]
    elif value in (2,3,4):
        return suf[2]
    return suf[3]
