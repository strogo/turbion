from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from turbion.bits.utils.decorators import paged, templated
from turbion.bits.utils.pagination import paginate

from turbion.bits.blogs.decorators import titled
from turbion.bits.blogs.models import Post

from datetime import date

@templated('turbion/blogs/archive.html')
@titled(page=_('Blog archive'))
def index(request):
    return {
        "posts": Post.published.all()
    }

@paged
@templated('turbion/blogs/archive_list.html')
@titled(page=_('Blog archive on {{ year }}'))
def year(request, year_id):
    post_page = paginate(
        Post.published.filter(published_on__year=year_id),
        request.page,
        settings.TURBION_BLOG_POSTS_PER_PAGE
    )

    return {
        "post_page": post_page,
        "on": "year",
        "year": year_id
    }

@paged
@templated('turbion/blogs/archive_list.html')
@titled(page=_('Blog archive on {{ year }}/{{ month }}'))
def month(request, year_id, month_id):
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
        "on": "month",
        "year": year_id,
        'month': month_id
    }

@paged
@templated('turbion/blogs/archive_list.html')
@titled(page=_('Blog archive on {{ year }}/{{ month }}/{{ day }}'))
def day(request, year_id, month_id, day_id):
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
        "on": "day",
        "year": year_id,
        'month': month_id,
        'day': day_id
    }
