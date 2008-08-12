# -*- coding: utf-8 -*-
from django import template
from django.template import resolve_variable, TemplateSyntaxError, Node
from django.utils.encoding import smart_str
from django.conf import settings
from django.db.models import signals
from django.db import connection
from django.contrib.contenttypes.models import ContentType

from turbion.blogs.models import Post, Comment
from turbion.profiles.models import Profile

from pantheon.cache.tags import cached_inclusion_tag

register = template.Library()

quote_name = connection.ops.quote_name

posts_table_name    = quote_name(Post._meta.db_table)
comments_table_name = quote_name(Comment._meta.db_table)
profiles_table_name = quote_name(Profile._meta.db_table)

@cached_inclusion_tag(register,
                      trigger = { "sender" : Post,
                                  "signal" : signals.post_save,
                                  "suffix" : lambda instance, created, *args, **kwargs: instance.blog.id },
                      suffix = lambda context, blog: blog.id,
                      file_name='turbion/blogs/pads/archive_pad.html',
                      takes_context=True)
def archive_pad( context, blog ):
    months = Post.published.for_blog(blog).dates("created_on", "month", order='DESC').distinct()

    return {
        'blog': blog,
        'months': months,
    }

@cached_inclusion_tag(register,
                      trigger={"sender": Comment,
                               "signal": signals.post_save,
                               "suffix": lambda instance, *args, **kwargs: instance.connection.blog.id},
                      suffix=lambda context, blog: blog.id,
                      file_name='turbion/blogs/pads/top_commenters_pad.html',
                      takes_context=True)
def top_commenters_pad(context, blog, count=5):
    ct = ContentType.objects.get_for_model(Post)
    extra_where = [ "%s.id = %s.created_by_id" % (users_table_name, comments_table_name),
                    "%s.connection_ct_id = %s " % (comments_table_name, ct.id),
                    "%s.blog_id = %s" % (posts_table_name, blog._get_pk_val())
                     ]

    return  {"commenters": Profile.objects.select_related()\
             .extra(select={"comment_count": "SELECT COUNT(*) FROM %s as cc WHERE cc.created_by_id = turbion_profile.id" % (comments_table_name, profiles_table_name)} )\
             .extra(where=extra_where, tables=[comments_table_name, posts_table_name])\
             .order_by('-comment_count').distinct()[:count]}


@cached_inclusion_tag(register,
                      trigger = { "sender" : Comment,
                                  "signal" : signals.post_save,
                                  "suffix" : lambda instance, *args, **kwargs: instance.connection.blog.id },
                      suffix = lambda context, blog: blog.id,
                      file_name='turbion/blogs/pads/last_comments_pad.html',
                      takes_context=True)
def last_comments_pad(context, blog, count=5):
    comments = Comment.published.for_model_with_rel(Post, blog).order_by("-created_on").distinct()[:count]

    return  { "comments" : comments }

@cached_inclusion_tag(register,
                      trigger={"sender": Post,
                               "signal": signals.post_save,
                               "suffix": lambda instance, created, *args, **kwargs: instance.blog.id},
                      suffix=lambda context, blog: blog.id,
                      file_name='turbion/blogs/pads/top_posts_pad.html',
                      takes_context=True)
def top_posts_pad(context, blog, count=5):
    return  {"posts": Post.published.for_blog(blog).order_by('-comment_count')[:count]}

@cached_inclusion_tag(register,
                      trigger={"sender": Post,
                                "signal": signals.post_save,
                                "suffix": lambda instance, created, *args, **kwargs: instance.blog.id},
                      suffix = lambda context, blog: blog.id,
                      file_name='turbion/blogs/pads/tags_pad.html',
                      takes_context=True)
def tags_pad(context, blog):
    return {"blog": blog,
            "tags" : blog.tags
        }

@cached_inclusion_tag(register,
                      trigger={"sender": Post,
                               "signal": signals.post_save,
                               "checker":  lambda *args,**kwargs: True },
                      suffix=lambda context, blog: ( blog.id, blog.calendar.current ),
                      file_name='turbion/blogs/pads/calendar_pad.html',
                      takes_context=True)
def calendar_pad(context, blog):
    return {"blog": blog}

@cached_inclusion_tag(register,
                      trigger={"sender" : Post,
                                "signal" : signals.post_save,
                                "checker" :  lambda  *args,**kwargs: True },
                      suffix=lambda context, post: [post.blog.id, post.id],
                      file_name='turbion/blogs/pads/prevnext_pad.html',
                      takes_context=True)
def prevnext_pad(context, post):
    filter = Post.published.lookups
    try:
        prev_post = post.get_previous_by_created_on(**filter)
    except Post.DoesNotExist:
        prev_post = None

    try:
        next_post = post.get_next_by_created_on(**filter)
    except Post.DoesNotExist:
        next_post = None

    return {"prev_post": prev_post,
            "next_post": next_post}
