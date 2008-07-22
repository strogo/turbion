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
from turbion.assets.models import Asset

@never_cache
@blog_view
@templated("turbion/dashboard/assets/assets.html")
@titled()
def index( request, blog ):
    return {"blog": blog}

@never_cache
@blog_view
@templated("turbion/dashboard/form.html")
@titled()
def edit(request, blog, asset_id=None):
    if asset_id:
        asset = get_object_or_404(Asset.objects.for_object(blog), pk=asset_id)
    else:
        asset = None
    
    if request.POST:
        form = AssetForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            new_asset = form.save(False)
            if not asset:
                new_asset.created_by = request.user.profile
            else:
                new_asset.edited_by = request.user.profile
            new_asset.save()
            
            new_asset.connect_to(blog)
            
            form.postprocess()
            
            return http.HttpResponseRedirect(reverse("dashboard_blog_assets", args=(blog.slug,)))
    else:
        form = AssetForm(instance=asset)

    return {"blog": blog,
            "form": form,
            "asset": asset }
    
    
@never_cache
@blog_view
def delete(request, blog, asset_id):
    asset = get_object_or_404(Asset.objects.for_object(blog), pk=asset_id)
    
    asset.delete()
    
    return http.HttpResponseRedirect(reverse("dashboard_blog_assets", args=(blog.slug,)))
    
