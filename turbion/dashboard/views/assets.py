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
from django.views.decorators.cache import never_cache

from pantheon.utils.decorators import titled, templated

from turbion.blogs.decorators import blog_view, post_view
from turbion.blogs.models import Blog, BlogRoles, Post, CommentAdd, Comment
from turbion.dashboard import forms
from turbion.profiles.models import Profile
from turbion.pingback import signals
from turbion.roles.decorators import has_capability_for

from turbion.assets.forms import AssetForm

@never_cache
@blog_view
@templated( "turbion/dashboard/assets/assets.html")
@titled()
def index( request, blog ):
    return {"blog": blog}

@never_cache
@blog_view
@templated( "turbion/dashboard/form.html")
@titled()
def new( request, blog ):
    if request.POST:
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            asset = form.save(False)
            asset.created_by = request.user.profile
            asset.save()
            
        print form.errors
    else:
        form = AssetForm()

    return {"blog": blog,
            "form": form}
