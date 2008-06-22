# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django import http
from django.core.urlresolvers import reverse

def has_capability_for( perm, obj_name = None, cond = "AND" ):
    def _wrapper( func ):
        def _decorator( request, *args, **kwargs ):
            if request.user.is_authenticated():
                if obj_name:
                    if callable( obj_name ):
                        obj = obj_name( request, *args, **kwargs )
                    else:
                        obj = kwargs[ obj_name ]
                else:
                    obj = None
                if request.user.profile.has_capability_for( perm, obj, cond ):
                    return func( request, *args, **kwargs )
            return http.HttpResponseRedirect( reverse("no_capability") )
        _decorator.perm = perm
        return _decorator
    return _wrapper
