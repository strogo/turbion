# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2008 Alexander Koshelev (daevaorn@gmail.com)
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def add_turbion_media( url ):
    return "%sturbion/%s" % ( settings.MEDIA_URL, url )
