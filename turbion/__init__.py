# -*- coding: utf-8 -*-

def prepare_turbion_settings(outer_settings, options):
    from django.conf import global_settings
    from django.core.exceptions import ImproperlyConfigured
    
    from turbion import settings

    result = {}
    
    options = dict([(key.upper(), value) for key, value in options.items()])
    
    for name in dir(settings):
        if name.upper() == name:
            if "TURBION_" in name:
                raw_name = name[8:]
                
                result[name] = options.pop(raw_name, getattr(settings, name))           
            else:
                base_value = outer_settings.get(name, getattr(global_settings, name, None))
                
                value = getattr(settings, name)
                
                if callable(value):
                    if base_value:
                        value = value(base_value)
                    else:
                        value = value()
                elif base_value:
                    raise ImproperlyConfigured("Settings value conflict for %s" % name)
                
                result[name] = value
    
    if options:
        result.update([("TURBION_%s" % key, value) for key, value in options.items()])
    
    return result
                
def configure(**options):
    import inspect
    
    outer_scope = inspect.stack()[1][0].f_locals
       
    outer_scope.update(prepare_turbion_settings(outer_scope, options))
