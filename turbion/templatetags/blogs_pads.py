from django import template
from django.conf import settings
from django.db.models import signals
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from turbion.bits.blogs.models import Post, Comment, Tag
from turbion.bits.utils.cache.tags import cached_inclusion_tag

register = template.Library()

D = dict

@cached_inclusion_tag(register,
                      trigger=D(
                        sender=Comment,
                        signal=signals.post_save,
                        suffix=lambda instance, *args, **kwargs: []
                      ),
                      suffix=lambda context: [],
                      file_name='turbion/blogs/pads/latest_comments.html',
                      takes_context=True)
def latest_comments_pad(context, count=5):
    comments = Comment.published.all().order_by("-created_on").distinct()[:count]

    return  {"comments": comments}

@cached_inclusion_tag(register,
                      trigger={"sender": Post,
                                "signal": signals.post_save,
                                "suffix": lambda instance, created, *args, **kwargs: []},
                      suffix=lambda contex: [],
                      file_name='turbion/blogs/pads/tags.html',
                      takes_context=True)
def tags_pad(context):
    return {
        "tags" : Tag.active.all(),
    }

@cached_inclusion_tag(register,
                      trigger=D(
                        sender=Post,
                        signal=signals.post_save,
                        checker=lambda *args,**kwargs: True
                      ),
                      suffix=lambda context, post: [post.id],
                      file_name='turbion/blogs/pads/prevnext.html',
                      takes_context=True)
def prevnext_pad(context, post):
    filter = Post.published.get_lookup()
    try:
        prev_post = post.get_previous_by_published_on(filter)
    except Post.DoesNotExist:
        prev_post = None

    try:
        next_post = post.get_next_by_published_on(filter)
    except Post.DoesNotExist:
        next_post = None

    return {
        "prev_post": prev_post,
        "next_post": next_post
    }

@register.inclusion_tag(
    file_name='turbion/blogs/pads/login.html',
    takes_context=True
)
def login_pad(context):
    from turbion.bits.profiles import get_profile
    urls = []
    user = get_profile(context["user"])

    if user.is_authenticated():
        if user.is_trusted():
            urls.append((_("Profile"), reverse('turbion_profile_edit')))
            urls.append((_("Watchlist"), reverse('turbion_watchlist')))
        urls.append((_("Logout"), reverse('django.contrib.auth.views.logout')))
    else:
        urls.append((_("OpenID login"), reverse("turbion_openid_login")))

    return {
        "user": user,
        "urls": urls
    }

@register.inclusion_tag(
    file_name='turbion/blogs/pads/search.html',
    takes_context=True
)
def search_pad(context):
    from turbion.bits.blogs.forms import SearchForm

    request = context.get("request")

    return {
        "request": request,
        "form": SearchForm(initial={"query": request and request.GET.get("query", "") or ""}),
        "action": reverse("turbion_blog_search")
    }
