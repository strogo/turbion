# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from turbion.blogs.decorators import blog_view, post_view, titled
from turbion.comments import views, models
from turbion.blogs.models import Post

from turbion.utils.decorators import templated, paged

@blog_view
@templated('turbion/blogs/edit_comment.html')
@titled(page=u'Добавление комментария к "{{post.title}}"')
def add(request, blog, post_id):
    post = get_object_or_404(Post.published.for_blog(blog), pk=post_id)

    if not post.allow_comments:
        return HttpResponseRedirect(post.get_absolute_url())#FIXME: add message showing

    context = views.add_comment(request,
                                connection=post,
                                defaults={})

    if isinstance(context, dict):
        context.update({"blog": blog,
                        "post": post,
                        "form_action": "./"
                      })
    return context

@blog_view
@templated('turbion/blogs/edit_comment.html')
@titled(page=u'Редактирование комментария к "{{post.title}}"')
def edit(request, blog, comment_id):
    comment = get_object_or_404(models.Comment.published,  pk=comment_id)
    post = comment.connection
    context = views.edit_comment(request,
                                 comment=comment,
                                 redirect=post.get_absolute_url()+"#comment_%(id)s",
                                 checker=lambda comment: request.user in (comment.author, post.created_by))

    if isinstance(context, dict):
        context.update({"blog": blog, "post": post})
    return context
