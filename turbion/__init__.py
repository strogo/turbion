# -*- coding: utf-8 -*-
from django.conf import global_settings

from turbion import settings

def configure(**options):
    import inspect

    settings_scope = inspect.stack()[1][0].f_locals

    for name in dir(settings):
        if name.upper() == name:
            if "TURBION_" in name:
                raw_name = name[8:]
            else:
                raw_name = name

            
