from django.conf import settings
from django import template
from django.template.loader import render_to_string
from django.utils.http import urlencode
from django.utils.encoding import smart_str

from turbion.core.utils.pagination import split_domains

register = template.Library()

@register.simple_tag
def paginator(page, template="paginator.html", head_num=2, tail_num=1, left_num=1, right_num=2):
    if page.paginator.num_pages == 1:
        return ""

    head, center, tail = split_domains(page.number, page.paginator.num_pages,
                                       head_num, tail_num, left_num, right_num)

    context = {
        'page': page,
        'head': head,
        'center': center,
        'tail': tail
    }
    return  render_to_string(template, context)

class QueryNode(template.Node):
    def __init__(self, kwargs):
        self.kwargs = kwargs

    def render(self, context):
        request = context['request']

        data = request.GET.copy()
        data.update(
            dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])
        )

        if data:
            return '?' + urlencode(dict([(k, v) for k, v in data.iteritems() if v not in (None, '')]))
        else:
            return ''

@register.tag
def query(parser, token):
    bits = token.contents.split(' ')
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes one argument"
                                  " (list of name=value pairs)" % bits[0])

    kwargs = {}

    for arg in bits[1].split(","):
        if '=' in arg:
            k, v = arg.split('=', 1)
            k = k.strip()
            kwargs[k] = parser.compile_filter(v)

    return QueryNode(kwargs)
