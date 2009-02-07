from django.utils.translation import ugettext_lazy as _
from django.db import models

from turbion.core.utils._calendar import Calendar
from turbion.core.blogs.models import Post

class BlogCalendar(Calendar):
    date_field = "published_on"
    queryset = Post.published.all()

    @models.permalink
    def get_month_url(self, date):
        return "turbion_blog_archive_month", (date.year, date.month), {}

    def get_per_day_urls(self, dates):
        return dict(
            [
                (
                    date.date(),
                    reverse(
                        "turbion_blog_archive_day",
                        args=(
                            date.year,
                            date.month,
                            date.day
                        )
                    )
                ) for date in dates
            ]
        )
