# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404

from turbion.core.utils.decorators import templated, titled

from turbion.core.staticpages.models import Page

@templated('turbion/staticpages/page.html')
@titled(page=u"{{page.title}}")
def dispatcher(request, slug):
    page = get_object_or_404(Page.published, slug=slug)

    return {
        "page": page,
    }, page.template or 'turbion/staticpages/page.html'
