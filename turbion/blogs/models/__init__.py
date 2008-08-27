# -*- coding: utf-8 -*-
from turbion.blogs.models.blog import Blog, BlogRoles
from turbion.blogs.models.post import Post, Comment

from django.conf import settings

if settings.TURBION_USE_DJAPIAN:
    import turbion.blogs.models.indexer
    import turbion.comments.indexer
