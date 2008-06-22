# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django import template
from django.utils import http
from django.contrib.sites.models import Site

from turbion.socialbookmarks.models import Group

register = template.Library()

@register.simple_tag
def socialbookmarks_fill_pattern( pattern, title, url, domain ):
    return pattern % { "title" : http.urlquote( title ), "url" : "http://%s%s" % ( domain, http.urlquote( url ) ) }

@register.inclusion_tag( 'socialbookmarks/group.html', takes_context=True )
def socialbookmarks_group( context, group_name, title, url ):
    if isinstance( group_name, basestring ):
        try:
            group = Group.objects.get( name = group_name )
        except Group.DoesNotExist:
            return {}
    else:
        group = group_name
    
    domain = Site.objects.get_current().domain    
    
    return { "group" : group,
            "title": title,
            "url":url,
            "domain":domain }