# -*- coding: utf-8 -*-
from django.conf import settings

from djapian import Indexer

indexer = Indexer(model="comments.Comment",
                  fields=("text",),
                  tags=[
                        ("created_by", "created_by"),
                    ]
            )
