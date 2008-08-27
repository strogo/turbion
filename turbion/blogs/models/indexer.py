# -*- coding: utf-8 -*-
from django.conf import settings

from turbion.blogs.models.post import Post

from djapian import Indexer

indexer = Indexer(model=Post,
                  fields=("text",),
                  tags=[
                        ("blog",   "blog.slug"),
                        ("status", "status"),
                        ("title",  "title")
                    ],
                  trigger=(lambda post: post.is_published)
        )
