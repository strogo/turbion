# -*- coding: utf-8 -*-
from django.conf import settings

from turbion.comments.models import Comment

from djapian import Indexer

indexer = Indexer(model=Comment,
                  fields=("text",),
                  tags=[
                        ("created_by", "created_by"),
                    ]
            )
