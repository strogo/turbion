# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007-2008 Alexander Koshelev (daevaorn@gmail.com)
from pantheon.utils.tags import simple_tag_with_request
from django import template

register = template.Library()

@simple_tag_with_request( register )
def post_action( request, post, action ):
    return post.get_absolute_url() + action + "/?redirect=" + request.build_absolute_uri()

@simple_tag_with_request( register )
def post_form_action( request, url ):
    return url + "?redirect=" + request.GET.get( 'redirect', request.build_absolute_uri() )