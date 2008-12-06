# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import signals

from turbion.utils.composition import CompositionField
from turbion.comments.models import Comment

D = dict

class CommentCountField(CompositionField):
    def __init__(self, verbose_name=None, editable=False):
        super(CommentCountField, self).__init__(
            native=models.PositiveIntegerField(
                default=0, editable=editable, verbose_name=verbose_name
            ),
            trigger=[
                D(
                    on=(signals.post_save, signals.post_delete),
                    do=lambda host, comment, signal: Comment.published.for_object(host).count()
                )
            ],
            commons=D(
                sender_model=Comment,
                field_holder_getter=lambda comment: comment.connection,
            ),
            commit=True,
            update_method=D(
                do=0,
                initial=0,
                queryset=lambda host: Comment.published.for_object(host).count(),
                name="sync_comment_count"
            )
        )
