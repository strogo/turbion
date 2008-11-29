# -*- coding: utf-8 -*-
from django.conf import settings

from djapian import Indexer

indexer = Indexer(model="blogs.Post",
                  fields=("text",),
                  tags=[
                        ("blog",   "blog.slug"),
                        ("status", "status"),
                        ("title",  "title")
                  ],
                  trigger=(lambda post: post.is_published)
        )
