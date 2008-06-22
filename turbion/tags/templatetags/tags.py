# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django import template

from turbion.links.models import Link
from turbion.tags.models import Tag

register = template.Library()

@register.simple_tag
def tag_ratio( tag, count, all_count , max = 30, min = 10):
    return min + count * max / all_count