# -*- coding: utf-8 -*-
#--------------------------------
#$Date: 2008-03-24 00:39:53 +0300 (Mon, 24 Mar 2008) $
#$Author: daev $
#$Revision: 1217 $
#--------------------------------
#Copyright (C) 2007-2008 Alexander Koshelev (daevaorn@gmail.com)
from pantheon.cache.utils import CacheWrapper

def cached( trigger, suffix = None, base_name = None ):
    def _wrapper( func ):
        if base_name == None:
            real_base_name = func.__module__ + "." + func.__name__
        else:
            real_base_name = base_name

        return CacheWrapper( func, trigger, suffix, real_base_name )
    return _wrapper