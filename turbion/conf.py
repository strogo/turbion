# -*- coding: utf-8 -*-
from django.utils.functional import curry

def to_list(func):
    def _decorator(value, *args, **kwargs):
        if isinstance(value, tuple):
            value = list(value)
        elif isinstance(value, list):
            pass
        else:
            raise ValueError

        return func(value, *args, **kwargs)
    return _decorator

def _append(source, value, functor):
    return value + [s for s in source if functor(s)]

def _insert(source, value, functor):
    for pos, klass in source:
        if not functor(klass):
            continue
        if pos is not None:
            if isinstance(pos, basestring):
                try:
                    i = value.index(pos)
                    value[i] = klass
                except ValueError:
                    value.append(klass)
            else:
                value.insert(pos, klass)
        else:
            value.append(klass)
    return value

def merge(source):
    @to_list
    def _func(value, functor=lambda x: True):
        if len(source):
            elem = source[0]
            if isinstance(elem, (list, tuple)):
                return _insert(source, value, functor)
            else:
                return _append(source, value, functor)
        else:
            return value
    return _func

class GenericConfigurator(object):
    def __init__(self, settings, prefix):
        self.local_settings = settings
        self.prefix = prefix

    def prepare_settings(self, outer_settings, options):
        from django.conf import global_settings
        from django.core.exceptions import ImproperlyConfigured

        result = {}

        options = dict([(key.upper(), value) for key, value in options.items()])

        for name in dir(self.local_settings):
            if name.upper() == name:
                if name.startswith(self.prefix):
                    raw_name = name[len(self.prefix):]

                    result[name] = options.pop(raw_name, getattr(self.local_settings, name))
                else:
                    base_value = outer_settings.get(name, getattr(global_settings, name, None))

                    value = getattr(self.local_settings, name)

                    if callable(value):
                        handler_name = "handle_%s" % name.lower()
                        handler = curry(getattr(self, handler_name, lambda x, options: True), options=options)

                        if base_value:
                            value = value(base_value, handler)
                        else:
                            value = value(handler)
                    elif base_value:
                        raise ImproperlyConfigured("Settings value conflict for %s" % name)

                    result[name] = value

        if options:
            result.update([("%s%s" % (self.prefix, key), value) for key, value in options.items()])

        return result

    def __call__(self, **options):
        import inspect

        outer_scope = inspect.stack()[1][0].f_locals

        outer_scope.update(self.prepare_settings(outer_scope, options))
