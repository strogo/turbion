# -*- coding: utf-8 -*-
from django import template
from django.template.loader import render_to_string
from django.utils.dates import WEEKDAYS

register = template.Library()

@register.simple_tag
def calendar(cal, tmpl):
    context = {
        'calendar': cal,
        "weekdays": WEEKDAYS.values()
    }
    return render_to_string(tmpl, context)
