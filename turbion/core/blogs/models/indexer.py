# -*- coding: utf-8 -*-
from django.conf import settings

from djapian import Indexer

indexer = Indexer(model="turbion.Post",
                  fields=("text",),
                  tags=[
                        ("status", "status"),
                        ("title",  "title")
                  ],
                  trigger=(lambda post: post.is_published)
        )

indexer = Indexer(model="turbion.Comment",
                  fields=("text",),
                  tags=[
                        ("created_by", "created_by"),
                    ]
            )
