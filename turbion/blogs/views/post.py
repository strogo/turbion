# -*- coding: utf-8 -*-
from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from turbion.blogs.decorators import blog_view, post_view, login_required, titled
from turbion.blogs.models import Blog, Post, Comment
from turbion.profiles.models import Profile
from turbion.blogs.utils import blog_reverse
from turbion.comments import forms as comments_forms

from turbion.tags.models import Tag

from turbion.utils.pagination import paginate
from turbion.utils.decorators import paged, templated

@blog_view
@paged
@templated('turbion/blogs/list.html')
@titled(page=u'Блог')
def blog(request, blog):
    blog.inc_reviews()

    posts = Post.published.for_blog(blog)

    if not request.user.is_authenticated_confirmed():
        posts = posts.filter(showing=Post.show_settings.everybody)

    post_paginator = paginate(posts,
                              request.page,
                              blog.post_per_page)

    context = {"blog": blog,
            "post_paginator": post_paginator}

    return context

@blog_view
@paged
@templated('turbion/blogs/tags.html')
@titled(page=u'Теги')
def tags(request, blog):
    _tags = blog.tags

    return {"blog": blog,
            "tags": _tags,
            }
@blog_view
@paged
@templated('turbion/blogs/list.html')
@titled(page=u'Тег "{{tag}}"')
def tag(request, blog, tag_slug):
    _tag = get_object_or_404(blog.tags, slug=tag_slug)
    posts = Post.published.for_tag(blog, _tag)

    if not request.user.is_authenticated_confirmed():
        posts = posts.filter(showing=Post.show_settings.everybody)

    post_paginator = paginate(posts,
                              request.page,
                              blog.post_per_page)

    return {"blog": blog,
            "tag": _tag,
            "post_paginator": post_paginator
            }

@blog_view
@post_view
@templated('turbion/blogs/post.html')
@titled(page='{{post.title}}')
def post(request, blog, post):
    post.inc_reviews()
    comment_form = comments_forms.CommentForm(request=request)
    form_action = blog_reverse("blog_comment_add", args=(post.blog.slug, post.id))

    comments = Comment.published.for_object(post).select_related("created_by").order_by("created_on")

    return {"blog": blog,
            "post": post,
            "comments": comments,
            "comment_form": comment_form,
            "form_action": form_action }
