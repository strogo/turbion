# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import *
from django.contrib.auth.models import User
from django.dispatch import dispatcher


from turbion.blogs.decorators import blog_view, post_view, login_required, title_bits
from turbion.blogs.models import Blog, Post, Comment
from turbion.profiles.models import Profile
from turbion.blogs.utils import blog_reverse
from turbion.comments import forms as comments_forms

from turbion.tags.models import Tag
from turbion.pingback import signals

from pantheon.utils.paging import paginate
from pantheon.utils.decorators import paged, render_to

@blog_view
@paged
@title_bits( page = u'Блог' )
@render_to( 'blogs/list.html' )
def blog( request, blog ):
    blog.inc_reviews()

    post_paginator = paginate( Post.published.for_blog( blog ),
                              request.page,
                              blog.post_per_page )

    context = { "blog" : blog,
            "post_paginator" : post_paginator }

    return context

@blog_view
@paged
@title_bits( page=u'Теги')
@render_to( 'blogs/tags.html' )
def tags( request, blog ):
    _tags = blog.tags

    return { "blog" : blog,
            "tags" : _tags,
            }
@blog_view
@paged
@title_bits( page=u'Тег "{{tag}}"' )
@render_to( 'blogs/list.html' )
def tag( request, blog, tag_slug ):
    _tag = get_object_or_404( blog.tags, slug = tag_slug )
    posts = Post.published.for_tag( blog, _tag )

    post_paginator = paginate( posts,
                               request.page,
                               blog.post_per_page )

    return { "blog" : blog,
             "tag" : _tag,
             "post_paginator" : post_paginator
            }

@blog_view
@post_view
@title_bits( page='{{post.title}}' )
@render_to( 'blogs/post.html' )
def post( request, blog, post ):
    post.inc_reviews()
    comment_form = comments_forms.CommentForm( request = request )
    form_action = blog_reverse( "blog_comment_add", args = ( post.blog.slug, post.id ) )

    comments = Comment.published.for_object( post )

    return {"blog" : blog,
            "post" : post,
            "comments" : comments,
            "comment_form" : comment_form,
            "form_action": form_action }
