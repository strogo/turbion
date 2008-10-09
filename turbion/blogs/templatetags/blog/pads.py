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
from turbion.utils.cache.tags import cached_inclusion_tag

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
                               "signal": (signals.post_save, signals.post_delete),
                               "suffix": lambda instance, *args, **kwargs: instance.connection.blog.id},
                      suffix=lambda context, blog: blog.id,
                      file_name='turbion/blogs/pads/top_commenters_pad.html',
                      takes_context=True)
def top_commenters_pad(context, blog, count=5):
    ct = ContentType.objects.get_for_model(Post)

    extra_select="""
            SELECT COUNT(*)
            FROM %(comment_table)s AS cc, %(post_table)s AS pp
            WHERE cc.connection_ct_id=%(ct_id)s
                    AND cc.connection_id=pp.%(post_pk_name)s
                    AND cc.created_by_id=%(profile_table)s.%(profile_pk_name)s
                    AND pp.blog_id=%(blog_id)s
                    AND pp.created_by_id!=cc.created_by_id
    """ % {
        "comment_table": comments_table_name,
        "ct_id": ct._get_pk_val(),
        "blog_id": blog._get_pk_val(),
        "profile_table": profiles_table_name,
        "profile_pk_name": Profile._meta.pk.attname,
        "post_table": posts_table_name,
        "post_pk_name": Post._meta.pk.attname
    }

    return  {"commenters": Profile.objects.select_related()\
             .extra(select={"comment_count": extra_select} )\
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
