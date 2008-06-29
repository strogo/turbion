# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2008 Alexander Koshelev (daevaorn@gmail.com)
from django import http

from pantheon.utils.decorators import titled, templated

from turbion.blogs.decorators import blog_view, post_view
from turbion.blogs.models import Blog, BlogRoles, Post, CommentAdd
from turbion.blogs.dashboard import forms
from turbion.profiles.models import Profile

from turbion.roles.decorators import has_capability_for

@templated( "turbion/blogs/dashboard/blog/dashboard.html" )
@titled( page = "Dashboard", section = "Administration" )
@blog_view
@has_capability_for( BlogRoles.capabilities.enter_dashboard, "blog" )
def index( request, blog ):

    return { "blog" : blog }

@templated( "turbion/blogs/dashboard/blog/posts.html" )
@titled( page = "Dashboard", section = "Administration" )
@blog_view
@has_capability_for( BlogRoles.capabilities.enter_dashboard, "blog" )
def posts( request, blog ):
    posts = Post.objects.for_blog( blog ).order_by( "-created_on" )

    return { "blog"  : blog,
             "posts" : posts }

@templated( "turbion/blogs/dashboard/blog/table.html" )
@titled( page = "Dashboard", section = "Administration" )
@blog_view
@has_capability_for( BlogRoles.capabilities.enter_dashboard, "blog" )
def comments( request, blog ):

    return { "blog" : blog }

@templated( "turbion/blogs/dashboard/blog/table.html" )
@titled( page = "Dashboard", section = "Administration" )
@blog_view
def preferences( request, blog ):

    return { "blog" : blog }

@templated( 'turbion/blogs/dashboard/blog/form.html' )
@titled( page=u'Редактирование поста "{{post.title}}"' )
@blog_view
@has_capability_for( BlogRoles.capabilities.add_post, "blog" )
def post_new( request, blog, post = None ):
    draft = post and post.draft
    if request.method == 'POST':
        form = forms.PostForm( data = request.POST, instance = post, blog = blog )
        if form.is_valid():
            if 'view' in request.POST:
                post = form.save( False )
            else:
                post = form.save( False )

                try:
                    post.blog
                except Blog.DoesNotExist:
                    post.blog = blog

                try:
                    post.created_by
                except Profile.DoesNotExist:
                    post.created_by = request.user.profile

                post.edited_by = request.user.profile

                if draft and not post.draft:#reset date of creation
                    post.created_on = datetime.now()

                post.save()
                form.save_tags()

                if post.publish and post.notify:
                    CommentAdd.subscribe( post.created_by, post )

                if post.publish:
                    dispatcher.send( signal = signals.send_pingback,
                                     sender = Post,
                                     instance = post,
                                     url = post.get_absolute_url(),
                                     text = post.html,
                                )

                return http.HttpResponseRedirect( post.get_absolute_url() )
    else:
        form = forms.PostForm( blog = blog, instance = post )

    form_action = './'

    return { "blog" : blog,
             "post" : post,
             "form" : form,
             "form_action" : form_action }

def post_edit( request, post_id, *args, **kwargs ):
    post = Post.objects.get( pk = post_id )

    return post_new( request, post = post, *args, **kwargs )
