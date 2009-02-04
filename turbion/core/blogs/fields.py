# -*- coding: utf-8 -*-
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
                    do=lambda host, comment, signal: host.comments.count()
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
