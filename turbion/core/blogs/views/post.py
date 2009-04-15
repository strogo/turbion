from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse

from turbion.core.blogs.decorators import post_view, login_required, titled
from turbion.core.blogs.models import Post, Comment, Tag
from turbion.core.profiles.models import Profile
from turbion.core.pingback.models import Pingback
from turbion.core.blogs import forms
from turbion.core.profiles import get_profile
from turbion.core.utils.pagination import paginate
from turbion.core.utils.decorators import paged, templated
from turbion.core.utils import antispam

@paged
@templated('turbion/blogs/post_list.html')
@titled(page=_('Blog'))
def blog(request):
    posts = Post.published.all()

    if not get_profile(request).is_trusted():
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
        "tags": Tag.active.all(),
    }

@paged
@templated('turbion/blogs/tag_list.html')
@titled(page=_('Tag "{{tag}}"'))
def tag(request, tag_slug):
    _tag = get_object_or_404(Tag.active, slug=tag_slug)
    posts = _tag.posts.all()

    if not get_profile(request).is_trusted():
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
    comment_form = forms.CommentForm(request=request)
    antispam.process_form_init(request, comment_form)

    comments = Comment.published.filter(post=post)\
                        .select_related("created_by", "post")\
                        .order_by("created_on")

    pingbacks = Pingback.objects.filter(
        post=post,
        incoming=True,
        finished=True,
    )

    return {
        "post": post,
        "comments": comments,
        'pingbacks': pingbacks,
        "comment_form": comment_form
    }
