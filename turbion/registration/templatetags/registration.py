# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.conf import settings
from django import template
from django.template.loader import get_template
from django.template import Context

from turbion.registration.forms import LoginForm

register = template.Library()

@register.tag( name = "login_form" )
def login_form_tag( parser, token ):
    tag_name, template = token.split_contents()
    return LoginFormNode( template.strip( '"' ) )

class LoginFormNode(template.Node):
    def __init__( self, template):
         self.template = template
    
    def render( self, context ):
        template = get_template( self.template )
        
        if context.get( 'login_form', False ):
            return ""
        
        user = context[ 'user' ]
        
        if not user.is_authenticated():
            form_action = '/registration/login/?redirect=%s' % context[ 'request' ].build_absolute_uri()
        else:
            form_action = '/registration/logout/?redirect=%s' % context[ 'request' ].build_absolute_uri()

        return template.render( Context( { 'form' : LoginForm(),
                                          'user' : user,
                                          'form_action' : form_action,
                                          'request' : context[ 'request' ]
                                           } ) )