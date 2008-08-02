# -*- coding: utf-8 -*-
import re

from django import template

register = template.Library()

CAP_RE = re.compile( "(.*)\.(capabilities|roles)\.(.*)" )

class IfHasCapNode(template.Node):
    def __init__(self, caps, obj, cond, nodelist_true, nodelist_false ):
        self.caps = caps
        self.obj = obj
        self.cond = cond
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return "<IfHasCap node>"

    def __iter__(self):
        for node in self.nodelist_true:
            yield node
        for node in self.nodelist_false:
            yield node

    def render(self, context):
        user = context["user"]

        if user.is_authenticated():
            profile = user
            caps = []

            for cap in self.caps:
                try:
                    path, attr, name = CAP_RE.match(cap).groups()

                    module, set_name = path.rsplit(".", 1)

                    mod = __import__(module, {}, {}, [''])

                    role_set = getattr( mod, set_name )
                    manager  = getattr( role_set, attr )

                    caps.append( getattr( manager, name ) )
                except ( AttributeError, ImportError ):
                    raise template.TemplateSyntaxError

            if self.obj:
                obj = self.obj.resolve( context, True )
            else:
                obj = None
            cond = self.cond.resolve( context, True )

            if profile.has_capability_for( caps, obj, cond ):
                return self.nodelist_true.render(context)

        return self.nodelist_false.render(context)

@register.tag(name="if_has_caps")
def if_has_capability(parser, token):
    """
    {% if_has_caps cap obj "OR" %}

    {% else %}

    {% end_if_has_caps %}
    """
    bits = token.contents.split()
    tag_name = bits[ 0 ]
    if len( bits ) < 2:
        raise template.TemplateSyntaxError("'%s' statement requires at least two arguments" % tag_name )
    caps = [ perm.strip() for perm in bits[ 1 ].split( "," ) ]
    obj = len( bits ) == 3 and parser.compile_filter( bits[ 2 ] ) or None
    cond = len( bits ) == 4 and parser.compile_filter( bits[ 3 ]  ) or parser.compile_filter( "and" )

    nodelist_true = parser.parse(('else', 'end_%s' % tag_name ))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('end_%s' % tag_name,))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()

    return IfHasCapNode( caps, obj, cond, nodelist_true, nodelist_false )
