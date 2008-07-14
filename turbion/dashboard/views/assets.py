# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2008 Alexander Koshelev (daevaorn@gmail.com)
from datetime import datetime

from django import http
from django.dispatch import dispatcher
from django.core.urlresolvers import reverse

from pantheon.utils.decorators import titled, templated

from turbion.blogs.decorators import blog_view, post_view
from turbion.blogs.models import Blog, BlogRoles, Post, CommentAdd, Comment
from turbion.dashboard import forms
from turbion.profiles.models import Profile
from turbion.pingback import signals
from turbion.roles.decorators import has_capability_for

def index( request, blog ):
    pass

def new( request, blog ):
    pass
