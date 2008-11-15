# -*- coding: utf-8 -*-
from django.conf import settings
from django import template
from django.template.loader import render_to_string

from turbion.utils.pagination import split_domains

register = template.Library()

@register.simple_tag
def paginator(page, template="paginator.html", head_num=2, tail_num=1, left_num=1, right_num=2):
    if page.paginator.num_pages == 1:
        return ""

    head, center, tail = split_domains(page.number, page.paginator.num_pages,
                                       head_num, tail_num, left_num, right_num)

    context = {
        'page': page,
        'head': head,
        'center': center,
        'tail': tail
    }
    return  render_to_string(template, context)
