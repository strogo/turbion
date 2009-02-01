# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from turbion.core.utils.decorators import paged, templated
from turbion.core.utils.pagination import paginate

from turbion.core.blogs.decorators import titled
from turbion.core.blogs.models import Post

from datetime import date

@templated('turbion/blogs/archive.html')
@titled(page=_('Blog archive'))
def index(request):
    return {
        "posts": Post.published.all()
    }

@paged
@templated('turbion/blogs/archive_list.html')
@titled(page=_('Blog archive on {{blog.calendar.current.year}}'))
def year(request, year_id):
    blog.calendar.current = date(year=int(year_id), month=1, day=1)
    post_page = paginate(
        Post.published.filter(published_on__year=year_id),
        request.page,
        settings.TURBION_BLOG_POSTS_PER_PAGE
    )

    return {
        "post_page": post_page,
        "blog": blog
    }

@paged
@templated('turbion/blogs/archive_list.html')
@titled(page=_('Blog archive on {{blog.calendar.current.year}}/{{blog.calendar.current.month}}'))
def month(request, year_id, month_id):
    blog.calendar.current = date(year=int(year_id), month=int(month_id), day=1)
    post_page = paginate(
        Post.published.filter(
            published_on__year=int(year_id),
            published_on__month=int(month_id)
        ),
        request.page,
        settings.TURBION_BLOG_POSTS_PER_PAGE
    )

    return {
        "post_page" : post_page,
    }

@paged
@templated('turbion/blogs/archive_list.html')
@titled(page=_('Blog archive on {{blog.calendar.current.year}}/{{blog.calendar.current.month}}/{{blog.calendar.current.day}}'))
def day(request, year_id, month_id, day_id):
    blog.calendar.current = date(year=int(year_id), month=int(month_id), day=int(day_id))
    post_page = paginate(
        Post.published.filter(
            published_on__year=year_id,
            published_on__month=month_id,
            published_on__day=day_id
        ),
        request.page,
        settings.TURBION_BLOG_POSTS_PER_PAGE
    )

    return {
        "post_page": post_page,
    }
