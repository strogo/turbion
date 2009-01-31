# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404

from turbion.core.utils.decorators import templated, titled

from turbion.core.staticpages.models import Page
from turbion.core.blogs.decorators import blog_view

@templated('turbion/staticpages/page.html')
@titled(page=u"{{page.title}}")
@blog_view
def dispatcher(request, blog, slug):
    page = get_object_or_404(Page.published, blog=blog, slug=slug)

    return {
        "page": page,
        "blog": blog
    }, page.template or 'turbion/staticpages/page.html'
