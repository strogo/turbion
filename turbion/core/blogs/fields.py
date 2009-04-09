from django.db import models
from django.db.models import signals

from turbion.core.utils.composition import CompositionField

D = dict

class CommentCountField(CompositionField):
    def __init__(self, verbose_name=None, editable=False):
        from turbion.core.blogs.models.comment import Comment

        super(CommentCountField, self).__init__(
            native=models.PositiveIntegerField(
                default=0, editable=editable, verbose_name=verbose_name
            ),
            trigger=[
                D(
                    on=(signals.post_save, signals.post_delete),
                    do=lambda host, comment, signal: host.comments.filter(**Comment.published.lookups).count()
                )
            ],
            commons=D(
                sender_model=Comment,
                field_holder_getter=lambda comment: comment.post,
            ),
            commit=True,
            update_method=D(
                do=0,
                initial=0,
                queryset=lambda host: host.comments.count(),
                name="sync_comment_count"
            )
        )

class PostCountField(CompositionField):
    def __init__(self, verbose_name=None, editable=False):
        from turbion.core.blogs.models.post import Post

        super(PostCountField, self).__init__(
            native=models.PositiveIntegerField(
                default=0, editable=editable, verbose_name=verbose_name
            ),
            trigger=[
                D(
                    on=(signals.post_save, signals.post_delete),
                    do=lambda host, comment, signal: host.posts.filter(**Post.published.lookups).count()
                )
            ],
            commons=D(
                sender_model=Post,
                field_holder_getter=lambda post: post.tags.all(),
            ),
            commit=True,
            update_method=D(
                do=0,
                initial=0,
                queryset=lambda host: host.posts.count(),
                name="sync_post_count"
            )
        )
