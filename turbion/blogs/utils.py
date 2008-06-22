# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.core.urlresolvers import reverse
from django.conf import settings

def blog_reverse( viewname, urlconf=None, args=None, kwargs=None ):
    if not getattr( settings, 'BLOGS_MULTIPLE', False ):
        if args:
            args = list( args )
            del args[ 0 ]
        elif kwargs:
            kwargs.pop( "blog", None )
    url = reverse( viewname, urlconf, args, kwargs )

    return url.replace( "?", "" )

def permalink(func):
    def inner(*args, **kwargs):
        bits = func(*args, **kwargs)
        return blog_reverse(bits[0], None, *bits[1:3])
    return inner
