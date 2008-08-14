# -*- coding: utf-8 -*-
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse
from django.shortcuts import *
from django.http import Http404

from turbion.blogs.models import Comment, Post
from turbion.tags.models import Tag
from turbion.blogs import utils

from turbion.utils.title import gen_title

class BlogFieldBase(Feed):
    def __init__(self, blog, *args, **kwargs):
        self.blog = blog
        super(BlogFieldBase, self).__init__(*args, **kwargs)

class BasePostFeed(object):
    def item_link(self, post):
        return post.get_absolute_url()

    def item_pubdate(self, post):
        return post.created_on

    def item_author_name(self, post):
        return post.created_by.name

class PostsFeed(BasePostFeed, BlogFieldBase):
    description_template = "turbion/blogs/feeds/post_description.html"

    def title(self):
        return gen_title({"page":u"%s" % self.blog,
                          "section":u"Последние записи",
                          "site":""})

    def link(self):
        return self.blog.get_absolute_url()

    def description(self):
        return u'Последние записи блога "%s"' % self.blog

    def items(self):
        posts = Post.published.for_blog(self.blog)
        if not self.request.user.is_authenticated_confirmed():
            posts = posts.filter(showing=Post.show_settings.everybody)
        return posts

class PostsFeedAtom(PostsFeed):
    feed_type = Atom1Feed
    subtitle = PostsFeed.description

class CommentsFeed(BlogFieldBase):
    description_template = "turbion/blogs/feeds/comment_description.html"
    title_template = "turbion/blogs/feeds/comment_title.html"

    def get_object(self, bits):
        if len(bits) == 1:
            query_set = Post.published.for_blog(self.blog)
            if not self.request.user.is_authenticated_confirmed():
                query_set = query_set.filter(showing=Post.show_settings.everybody)
            return get_object_or_404(query_set,
                                     pk=bits[ 0 ])

    def title(self, post):
        return gen_title({"page":u"%s" % self.blog,
                          "section":u"Последнии комментарии" + (post and u' к "%s"' % post.title or ""),
                          "site":""})

    def link(self, post):
        return post and post.get_absolute_url() or self.blog.get_absolute_url()

    def description(self, post):
        if post:
            return u'Комментарии на "%s"' % post.title
        else:
            return u"Все комментарии"

    def item_pubdate(self, comment):
        return comment.created_on

    def item_link(self, comment):
        post = comment.connection
        return post.get_absolute_url() + "#comment_%s" % comment.id

    def item_author_name(self, comment ):
        return comment.created_by

    def items(self, post):
        return post and Comment.published.for_object(post).order_by("-created_on").distinct()\
                    or Comment.published.for_model_with_rel(Post, self.blog).order_by("-created_on").distinct()

class CommentsFeedAtom(CommentsFeed):
    feed_type = Atom1Feed
    subtitle = CommentsFeed.description

class TagFeed( BasePostFeed, BlogFieldBase):
    description_template = "turbion/blogs/feeds/tag_description.html"

    def get_object(self, bits):
        if len(bits) == 1:
            return get_object_or_404(self.blog.tags, slug =bits[0])
        raise Http404

    def title(self, tag):
        return gen_title({"page":u"%s" % self.blog,
                          "section":u"Последнии записи с тегом %s" % tag.name,
                          "site":""})

    def link(self, tag):
        return utils.blog_reverse("blog_tag", kwargs={"blog": self.blog.slug,
                                                      "tag_slug": tag.slug})

    def description(self, tag):
        return u"Посты с тегом %s" % tag.name

    def items(self, tag):
        return Post.published.for_tag(self.blog, tag)

class TagFeedAtom(TagFeed):
    feed_type = Atom1Feed
    subtitle = TagFeed.description
