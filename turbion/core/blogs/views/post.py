from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse

from turbion.core.blogs.decorators import post_view, login_required, titled
from turbion.core.blogs.models import Post, Comment
from turbion.core.profiles.models import Profile
from turbion.core.comments import forms as comments_forms
from turbion.core.tags.models import Tag
from turbion.core.profiles import get_profile
from turbion.core.utils.pagination import paginate
from turbion.core.utils.decorators import paged, templated

@paged
@templated('turbion/blogs/post_list.html')
@titled(page=_('Blog'))
def blog(request):
    posts = Post.published.all()

    if not get_profile(request).is_authenticated_confirmed():
        posts = posts.filter(showing=Post.show_settings.everybody)

    post_page = paginate(
        posts,
        request.page,
        settings.TURBION_BLOG_POSTS_PER_PAGE
    )

    context = {
        "post_page": post_page
    }

    return context

@paged
@templated('turbion/blogs/tags.html')
@titled(page=_('Tags'))
def tags(request):
    return {
        "tags": Tag.objects.for_model(Post),
    }

@paged
@templated('turbion/blogs/post_list.html')
@titled(page=_('Tag "{{tag}}"'))
def tag(request, tag_slug):
    _tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.published.for_tag(_tag)

    if not get_profile(request).is_authenticated_confirmed():
        posts = posts.filter(showing=Post.show_settings.everybody)

    post_page = paginate(
        posts,
        request.page,
        settings.TURBION_BLOG_POSTS_PER_PAGE
    )

    return {
        "tag": _tag,
        "post_page": post_page
    }

@post_view
@templated('turbion/blogs/post.html')
@titled(page='{{post.title}}')
def post(request, post):
    comment_form = comments_forms.CommentForm(request=request)

    comments = Comment.published.for_object(post)\
                        .select_related("created_by")\
                        .order_by("created_on")

    return {
        "post": post,
        "comments": comments,
        "comment_form": comment_form
    }
