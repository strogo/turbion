# -*- coding: utf-8 -*-
from django import template

from turbion.core.links.models import Link
from turbion.core.tags.models import Tag

register = template.Library()

@register.simple_tag
def tag_ratio( tag, count, all_count , max = 30, min = 10):
    return min + count * max / all_count
