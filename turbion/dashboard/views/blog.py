# -*- coding: utf-8 -*-
from datetime import datetime

from django import http
from django.dispatch import dispatcher
from django.core.urlresolvers import reverse

from pantheon.utils.decorators import titled, templated

from turbion.blogs.decorators import blog_view, post_view
from turbion.blogs.models import Blog, BlogRoles, Post, CommentAdd, Comment
from turbion.feedback.models import Feedback
from turbion.dashboard import forms
from turbion.profiles.models import Profile
from turbion.pingback import signals
from turbion.roles.decorators import has_capability_for

@templated( "turbion/dashboard/blogs/dashboard.html" )
@titled( page = "Dashboard", section = "Administration" )
@blog_view
@has_capability_for( BlogRoles.capabilities.enter_dashboard, "blog" )
def dashbaord( request, blog ):
    latest_posts = Post.objects.for_blog( blog ).order_by("-created_on")[:5]
    latest_comments = Comment.published.for_model_with_rel( Post, blog ).order_by("-created_on").distinct()[:5]
    latest_feedbacks = Feedback.new.all()

    return { "blog"            : blog,
             "latest_posts"    : latest_posts,
             "latest_comments" : latest_comments,
             "latest_feedback": latest_feedbacks }

@templated( "turbion/dashboard/blogs/posts.html" )
@titled( page = "Dashboard", section = "Administration" )
@blog_view
@has_capability_for( BlogRoles.capabilities.enter_dashboard, "blog" )
def index( request, blog ):
    posts = Post.objects.for_blog( blog ).order_by( "-created_on" )

    return { "blog"  : blog,
             "object_list" : posts }

@templated( "turbion/dashboard/table.html" )
@titled( page = "Dashboard", section = "Administration" )
@blog_view
@has_capability_for( BlogRoles.capabilities.enter_dashboard, "blog" )
def comments( request, blog ):

    return { "blog" : blog }

@templated( "turbion/dashboard/table.html" )
@titled( page = "Dashboard", section = "Administration" )
@blog_view
def preferences( request, blog ):

    return { "blog" : blog }

@templated('turbion/dashboard/form.html')
@titled(page=u'Редактирование поста "{{post.title}}"')
@blog_view
@has_capability_for(BlogRoles.capabilities.add_post, "blog")
def post_new(request, blog, post=None):
    was_draft = post and not post.is_published

    if request.POST:
        form = forms.PostForm(data=request.POST, instance=post, blog=blog)
        if form.is_valid():
            if 'view' in request.POST:
                new_post = form.save(False)
            else:
                new_post = form.save(False)
                new_post.blog = blog

                if not post:
                    new_post.created_by = request.user
                else:
                    new_post.edited_by = request.user

                if was_draft and new_post.is_published:#reset date of creation
                    new_post.created_on = datetime.now()

                new_post.save()
                form.save_tags()

                if new_post.is_published:
                    if new_post.notify:
                        CommentAdd.instance.subscribe(post.created_by, new_post)

                    dispatcher.send( signal = signals.send_pingback,
                                     sender = Post,
                                     instance = new_post,
                                     url = new_post.get_absolute_url(),
                                     text = new_post.text_html,
                                )

                return http.HttpResponseRedirect(reverse("dashboard_blog_posts", args = (blog.slug,)))
    else:
        form = forms.PostForm(blog=blog, instance=post)

    return { "blog": blog,
             "post": post,
             "form": form }

def post_edit(request, post_id, *args, **kwargs):
    post = Post.objects.get(pk = post_id)

    return post_new(request, post = post, *args, **kwargs)
