# -*- coding: utf-8 -*-
from django import template
from django.template import resolve_variable, TemplateSyntaxError, Node
from django.utils.encoding import smart_str
from django.conf import settings
from django.db.models import signals
from django.db import connection
from django.core.urlresolvers import reverse

from turbion.core.blogs.models import Post, Comment
from turbion.core.utils.cache.tags import cached_inclusion_tag

register = template.Library()

#@cached_inclusion_tag(register,
#                      trigger = { "sender" : Comment,
#                                  "signal" : m2m_post_save_reverse,
#                                  "suffix" : lambda instance, owner: [ owner.blog.id, owner.id ]},
#                      suffix = lambda context, post: [ context[ "user" ].is_author, post.blog.id, post.id ],
#                      file_name='blogs/include/comments.html',
#                      takes_context=True)
@register.inclusion_tag('turbion/blogs/include/comments.html', takes_context=True)
def post_comments(context, post):
    return {"post"    : post,
            "comments": Comment.published.for_object(post).select_related("created_by").order_by("created_on"),
            "user"    : context.get("user")
    }
