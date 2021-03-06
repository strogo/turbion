from django.db import models

from turbion.bits.utils.models import FilteredManager

class PostManager(FilteredManager):
    def get_query_set(self):
        return super(PostManager, self).get_query_set().select_related("created_by")

class TagManager(FilteredManager):
    def get_query_set(self):
        from turbion.bits.blogs.models import Post
        post_count = Post.published.count()

        if post_count != 0:
            total_ratio = float(super(TagManager, self).get_query_set().count()) / post_count
        else:
            total_ratio = 0

        return super(TagManager, self).get_query_set().extra(
            select={"ratio": "post_count * %s" % total_ratio}
        )

class CommentManager(FilteredManager):
    def get_query_set(self):
        return super(CommentManager, self).get_query_set().select_related("created_by")
