# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django import template
from django.template import Context
from django.template.loader import get_template
from django.utils.dates import WEEKDAYS

register = template.Library()

@register.simple_tag
def calendar( cal, tmpl, name = "calendar" ):
    tmpl = get_template( tmpl )
    context = Context( { 'calendar' : cal, "weekdays" : WEEKDAYS.values() } )
    return tmpl.render( context )