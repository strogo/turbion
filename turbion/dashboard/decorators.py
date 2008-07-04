# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.contrib.auth.decorators import user_passes_test


def data_response( func ):
    def _decor( reqest, *args, **kwargs ):
        pass
    return _decor

def is_superuser( user ):
    return user.is_staff and user.is_active and user.is_superuser

superuser_required = user_passes_test( is_superuser )
