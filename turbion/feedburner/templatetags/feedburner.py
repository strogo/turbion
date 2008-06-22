# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007-2008 Alexander Koshelev (daevaorn@gmail.com)
from django import template

from turbion.feedburner.models import Feed

register = template.Library()

@register.simple_tag
def feedburner_stat( ):