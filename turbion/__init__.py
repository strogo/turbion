# -*- coding: utf-8 -*-

def prepare_settings(outer_settings, options, local_settings, prefix):
    from django.conf import global_settings
    from django.core.exceptions import ImproperlyConfigured

    result = {}

    options = dict([(key.upper(), value) for key, value in options.items()])

    for name in dir(local_settings):
        if name.upper() == name:
            if name.startswith(prefix):
                raw_name = name[len(prefix):]

                result[name] = options.pop(raw_name, getattr(local_settings, name))
            else:
                base_value = outer_settings.get(name, getattr(global_settings, name, None))

                value = getattr(local_settings, name)

                if callable(value):
                    if base_value:
                        value = value(base_value)
                    else:
                        value = value()
                elif base_value:
                    raise ImproperlyConfigured("Settings value conflict for %s" % name)

                result[name] = value

    if options:
        result.update([("%s%s" % (prefix, key), value) for key, value in options.items()])

    return result

def generic_configurator(settings, prefix):
    def _configure(**options):
        import inspect

        outer_scope = inspect.stack()[1][0].f_locals

        outer_scope.update(prepare_settings(outer_scope, options, settings, prefix))
    return _configure

from turbion import settings

configure = generic_configurator(settings, "TURBION_")
