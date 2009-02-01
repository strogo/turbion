# -*- coding: utf-8 -*-
from django import template
from django.template import resolve_variable, TemplateSyntaxError, Node
from django.utils.encoding import smart_str
from django.conf import settings
from django.db.models import signals
from django.db import connection
from turbion.core.utils.descriptor import to_descriptor

from turbion.core.blogs.models import Post, Comment
from turbion.core.profiles.models import Profile
from turbion.core.tags.models import Tag
from turbion.core.utils.cache.tags import cached_inclusion_tag

register = template.Library()

quote_name = connection.ops.quote_name

posts_table_name    = quote_name(Post._meta.db_table)
comments_table_name = quote_name(Comment._meta.db_table)
profiles_table_name = quote_name(Profile._meta.db_table)

post_comments_filter = lambda comment: comment.connection_dscr == to_descriptor(Post)

D = dict

@cached_inclusion_tag(register,
                      trigger=D(
                            sender=Post,
                            signal=signals.post_save,
                            suffix=lambda instance, created, *args, **kwargs: []
                        ),
                      suffix=lambda context: [],
                      file_name='turbion/blogs/pads/archive.html',
                      takes_context=True)
def archive_pad(context):
    queryset = Post.published.all()

    class MonthMeta(object):
        def __init__(self, month):
            self.month = month

        def count(self):
            return queryset._clone().filter(
                        published_on__year=self.month.year,
                        published_on__month=self.month.month
            ).count()

    months = map(MonthMeta, queryset.dates("published_on", "month", order='DESC').distinct())

    return {
        'months': months,
    }

@cached_inclusion_tag(register,
                      trigger=D(
                        sender=Comment,
                        signal=(signals.post_save, signals.post_delete),
                        filter=post_comments_filter,
                        suffix=lambda instance, *args, **kwargs: [],
                  ),
                  suffix=lambda context: [],
                  file_name='turbion/blogs/pads/top_commenters.html',
                  takes_context=True)
def top_commenters_pad(context, count=5):
    dscr = to_descriptor(Post)

    extra_select="""
        SELECT COUNT(*)
        FROM %(comment_table)s AS cc, %(post_table)s AS pp
        WHERE cc.connection_dscr="%(dscr)s"
            AND cc.connection_id=pp.%(post_pk_name)s
            AND cc.created_by_id=%(profile_table)s.%(profile_pk_name)s
            AND pp.created_by_id!=cc.created_by_id
    """ % {
        "comment_table": comments_table_name,
        "dscr": dscr,
        "profile_table": profiles_table_name,
        "profile_pk_name": Profile._meta.pk.attname,
        "post_table": posts_table_name,
        "post_pk_name": Post._meta.pk.attname
    }

    return  {
        "commenters": Profile.objects.select_related()\
             .extra(select={"comment_count": extra_select})\
             .order_by('-comment_count').distinct()[:count]
    }

@cached_inclusion_tag(register,
                      trigger=D(
                        sender=Comment,
                        signal=signals.post_save,
                        filter=post_comments_filter,
                        suffix=lambda instance, *args, **kwargs: []
                      ),
                      suffix=lambda context: [],
                      file_name='turbion/blogs/pads/last_comments.html',
                      takes_context=True)
def last_comments_pad(context, count=5):
    comments = Comment.published.for_model(Post).order_by("-created_on").distinct()[:count]

    return  {"comments": comments}

@cached_inclusion_tag(register,
                      trigger=D(
                        sender= Post,
                        signal=signals.post_save,
                        suffix=lambda instance, created, *args, **kwargs: []
                        ),
                      suffix=lambda context: [],
                      file_name='turbion/blogs/pads/top_posts.html',
                      takes_context=True)
def top_posts_pad(context, count=5):
    return  {
        "posts": Post.published.all().order_by('-comment_count')[:count]
    }

@cached_inclusion_tag(register,
                      trigger={"sender": Post,
                                "signal": signals.post_save,
                                "suffix": lambda instance, created, *args, **kwargs: []},
                      suffix=lambda contex: [],
                      file_name='turbion/blogs/pads/tags.html',
                      takes_context=True)
def tags_pad(context):
    return {
        "tags" : Tag.objects.for_model(Post)
    }

@cached_inclusion_tag(register,
                      trigger=D(
                        sender=Post,
                        signal=(signals.post_save, signals.post_delete),
                        filter=lambda post: post.is_published,
                        suffix=lambda instance, *args, **kwargs: (instance.published_on.year, instance.published_on.month)
                      ),
                      suffix=lambda context: [],
                      file_name='turbion/blogs/pads/calendar.html',
                      takes_context=True)
def calendar_pad(context):
    return {"blog": None}

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
    filter = Post.published.lookups
    try:
        prev_post = post.get_previous_by_published_on(**filter)
    except Post.DoesNotExist:
        prev_post = None

    try:
        next_post = post.get_next_by_published_on(**filter)
    except Post.DoesNotExist:
        next_post = None

    return {
        "prev_post": prev_post,
        "next_post": next_post
    }
