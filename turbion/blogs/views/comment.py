# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from turbion.blogs.decorators import blog_view, post_view, title_bits
from turbion.comments import views, models
from turbion.blogs.models import Post

from pantheon.utils.decorators import render_to, paged

@blog_view
@title_bits( page = u'Добавление комментария к "{{post.title}}"' )
@render_to( 'blogs/edit_comment.html' )
def add( request, blog, post_id ):
    post = get_object_or_404( Post.published.for_blog( blog ), pk = post_id )

    context = views.add_comment( request,
                                 connection = post,
                                 defaults = { "postprocess" : blog.comments_default_postprocessor } )

    if isinstance( context, dict ):
        context.update( { "blog": blog,
                          "post" : post,
                          "form_action" : "./"
                        } )
    return context

@blog_view
@title_bits( page = u'Редактирование комментария к "{{post.title}}"' )
@render_to( 'blogs/edit_comment.html' )
def edit( request, blog, comment_id ):
    comment = get_object_or_404( models.Comment.published,  pk = comment_id )
    post = comment.connection
    context = views.edit_comment(request,
                                 comment = comment,
                                 redirect = post.get_absolute_url()+"#comment_%(id)s",
                                 checker = lambda comment: request.user in ( comment.author, post.created_by ) )

    if isinstance( context, dict ):
        context.update( { "blog": blog, "post" : post } )
    return context
