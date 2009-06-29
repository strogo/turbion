from django.db import models
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse
from django.shortcuts import *
from django import http
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from turbion.core.blogs.models import Comment, Post, Tag
from turbion.core.profiles import get_profile
from turbion.core.utils.title import gen_title

class BasePostFeed(Feed):
    def item_link(self, post):
        return post.get_absolute_url()

    def item_pubdate(self, post):
        return post.created_on

    def item_author_name(self, post):
        return post.created_by.name

class PostsFeed(BasePostFeed):
    description_template = "turbion/blogs/feeds/post_description.html"

    def title(self):
        return gen_title({
            "page": settings.TURBION_BLOG_NAME,
            "section": _("Latest entries")
        })

    @models.permalink
    def link(self):
        return ("turbion_blog_index",)

    def description(self):
        return _("Latest entries of blog '%s'") % settings.TURBION_BLOG_NAME

    def items(self):
        posts = Post.published.all().select_related()
        if not get_profile(self.request).is_trusted():
            posts = posts.filter(showing=Post.show_settings.everybody)
        return posts.order_by("-published_on")[:10]

class PostsFeedAtom(PostsFeed):
    feed_type = Atom1Feed
    subtitle = PostsFeed.description

class CommentsFeed(Feed):
    description_template = "turbion/blogs/feeds/comment_description.html"

    def get_object(self, bits):
        if len(bits) == 1:
            query_set = Post.published.all()
            if not get_profile(self.request).is_trusted():
                query_set = query_set.filter(showing=Post.show_settings.everybody)
            return get_object_or_404(query_set, pk=bits[0])

    def title(self, post):
        return gen_title({
            "page": settings.TURBION_BLOG_NAME,
            "section": _("Latest comments") + (post and " on '%s'" % post.title or "")
        })

    def link(self, post):
        return post and post.get_absolute_url() or reverse("turbion_blog_index")

    def description(self, post):
        if post:
            return _("Comments on '%s'") % post.title
        else:
            return _("Latest comments")

    def item_pubdate(self, comment):
        return comment.created_on

    def item_link(self, comment):
        return comment.get_absolute_url()

    def item_author_name(self, comment ):
        return comment.created_by

    def items(self, post):
        queryset = Comment.published.select_related()

        if post:
            comments = queryset.filter(post=post).order_by("-created_on").distinct()
        else:
            comments = queryset.all().order_by("-created_on").distinct()

        return comments[:50]

class CommentsFeedAtom(CommentsFeed):
    feed_type = Atom1Feed
    subtitle = CommentsFeed.description

class TagFeed(BasePostFeed):
    description_template = "turbion/blogs/feeds/post_description.html"

    def get_object(self, bits):
        if len(bits) == 1:
            return get_object_or_404(Tag.objects, slug=bits[0])
        raise http.Http404

    def title(self, tag):
        return gen_title({
            "page": settings.TURBION_BLOG_NAME,
            "section": _("Latest entries with tag '%s'") % tag.name
        })

    def link(self, tag):
        return reverse("turbion_blog_tag", args=(tag.slug,))

    def description(self, tag):
        return _("Entries with tag '%s'") % tag.name

    def items(self, tag):
        return Post.published.filter(tags=tag).select_related().distinct()[:10]

class TagFeedAtom(TagFeed):
    feed_type = Atom1Feed
    subtitle = TagFeed.description
