# -*- coding: utf-8 -*-
from django import template
from django.template import resolve_variable, TemplateSyntaxError, Node
from django.utils.encoding import smart_str
from django.conf import settings
from django.db.models import signals
from django.db import connection

from turbion.blogs.models import Post, Comment
from turbion.blogs.utils import blog_reverse
from turbion.utils.cache.tags import cached_inclusion_tag

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

@register.simple_tag
def tag_ratio( tag, blog, max = 30, min = 10 ):
    all_count = Post.published.for_blog( blog).count()
    count = 1#tag.post_count

    return min + count * max / all_count


class BlogURLNode(template.Node):
    def __init__(self, view_name, args, kwargs):
        self.view_name = view_name
        self.args = args
        self.kwargs = kwargs

    def render(self, context):
        from django.core.urlresolvers import NoReverseMatch
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])
        try:
            return blog_reverse(self.view_name, args=args, kwargs=kwargs)
        except NoReverseMatch:
            try:
                project_name = settings.SETTINGS_MODULE.split('.')[0]
                return blog_reverse(project_name + '.' + self.view_name,
                               args=args, kwargs=kwargs)
            except NoReverseMatch:
                return ''

@register.tag
def blog_url(parser, token):
    bits = token.contents.split(' ', 2)
    if len(bits) < 2:
        raise template.TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    args = []
    kwargs = {}
    if len(bits) > 2:
        for arg in bits[2].split(','):
            if '=' in arg:
                k, v = arg.split('=', 1)
                k = k.strip()
                kwargs[k] = parser.compile_filter(v)
            else:
                args.append(parser.compile_filter(arg))
    return BlogURLNode(bits[1], args, kwargs)
