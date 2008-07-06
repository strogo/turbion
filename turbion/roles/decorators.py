# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django import http
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

def has_capability_for( perm, obj_name = None, cond = "AND" ):
    def _wrapper( func ):
        @login_required
        def _decorator( request, *args, **kwargs ):
            if obj_name:
                if callable( obj_name ):
                    obj = obj_name( request, *args, **kwargs )
                else:
                    obj = kwargs[ obj_name ]
            else:
                obj = None
            if request.user.profile.has_capability_for( perm, obj, cond ):
                return func( request, *args, **kwargs )
            else:
                return http.HttpResponseRedirect( reverse("no_capability") )
        _decorator.perm = perm
        return _decorator
    return _wrapper
