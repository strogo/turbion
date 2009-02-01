# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from turbion.core.blogs.decorators import post_view, titled
from turbion.core.comments import views, models
from turbion.core.blogs.models import Post
from turbion.core.profiles import get_profile
from turbion.core.utils.decorators import templated, paged

@templated('turbion/blogs/edit_comment.html')
@titled(page=_('Add comment to "{{post.title}}"'))
def add(request, post_id):
    post = get_object_or_404(Post.published.all(), pk=post_id)

    if not post.allow_comments:
        return HttpResponseRedirect(post.get_absolute_url())#FIXME: add message showing

    context = views.add_comment(
        request,
        connection=post,
        status_getter=post.get_comment_status,
        next=post.get_absolute_url() + "#comment_%(id)s"
    )

    if isinstance(context, dict):
        context.update({
            "post": post,
        })

    return context

@templated('turbion/blogs/edit_comment.html')
@titled(page=_('Edit comment to "{{post.title}}"'))
def edit(request, comment_id):
    comment = get_object_or_404(models.Comment.published,  pk=comment_id)
    post = comment.connection

    context = views.edit_comment(
        request,
        comment=comment,
        redirect=post.get_absolute_url()+"#comment_%(id)s",
        checker=lambda comment: get_profile(request) in (comment.author, post.created_by)
    )

    if isinstance(context, dict):
        context.update({
            "post": post
        })
    return context
