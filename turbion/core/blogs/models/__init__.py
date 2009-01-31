# -*- coding: utf-8 -*-
from turbion.core.blogs.models.blog import Blog
from turbion.core.blogs.models.post import Post, Comment

from django.conf import settings

#if settings.TURBION_USE_DJAPIAN:
#    import turbion.core.blogs.models.indexer
#    import turbion.core.comments.indexer
