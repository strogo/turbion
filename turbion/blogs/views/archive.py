# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from turbion.utils.decorators import paged, templated
from turbion.utils.pagination import paginate

from turbion.blogs.decorators import blog_view, titled
from turbion.blogs.models import Post

from datetime import date

@blog_view
@templated('turbion/blogs/archive.html')
@titled(page=_('Blog archive'))
def index(request, blog):
    posts_query_set = Post.published.for_blog(blog)

    months = posts_query_set.dates("published_on", "month", order='DESC').distinct()

    posts = [(month, posts_query_set.filter(
                            published_on__year=month.year,
                            published_on__month=month.month)) for month in months]

    return {
        "months": months,
        "posts": posts,
        "blog": blog
    }

@blog_view
@paged
@templated('turbion/blogs/archive_list.html')
@titled(page=_('Blog archive on {{blog.calendar.current.year}}'))
def year(request, blog, year_id):
    blog.calendar.current = date(year=int(year_id), month=1, day=1)
    post_page = paginate(Post.published.for_blog(blog).filter(published_on__year=year_id),
                              request.page,
                              blog.post_per_page)

    return {
        "post_page": post_page,
        "blog": blog
    }

@blog_view
@paged
@templated('turbion/blogs/archive_list.html')
@titled(page=_('Blog archive on {{blog.calendar.current.year}}/{{blog.calendar.current.month}}'))
def month(request, blog, year_id, month_id):
    blog.calendar.current = date(year=int(year_id), month=int(month_id), day=1)
    post_page = paginate(Post.published.for_blog(blog).filter(published_on__year=int(year_id),
                                                                   published_on__month=int(month_id)),
                               request.page,
                               blog.post_per_page)

    return {
        "post_page" : post_page,
        "blog" : blog,
    }

@blog_view
@paged
@templated('turbion/blogs/archive_list.html')
@titled(page=_('Blog archive on {{blog.calendar.current.year}}/{{blog.calendar.current.month}}/{{blog.calendar.current.day}}'))
def day(request, blog, year_id, month_id, day_id):
    blog.calendar.current = date(year=int(year_id), month=int(month_id), day=int(day_id))
    post_page = paginate(Post.published.for_blog(blog).filter(published_on__year=year_id,
                                                                   published_on__month=month_id,
                                                                   published_on__day=day_id),
                              request.page,
                              blog.post_per_page)

    return {
        "post_page": post_page,
        "blog": blog,
    }
