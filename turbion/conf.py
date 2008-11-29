# -*- coding: utf-8 -*-
from django.utils.functional import curry

def to_list(value):
    """
        Converts sequence to list
    """
    if isinstance(value, tuple):
        value = list(value)
    elif isinstance(value, list):
        pass
    else:
        raise ValueError("Cannot convert %s to list" % value)

    return value

def module_to_dict(module):
    """
        Return dict of module uppercase attributes
    """
    return dict([(name, getattr(module, name))\
                   for name in dir(module) if name.upper() == name])

class Merge(object):
    """
        Helper class for merge settings sequence items
    """
    def __init__(self, settings, name):
        self.settings = to_list(settings)
        self.name = name

    def __call__(self, project_settings, global_settings, functor=lambda x: True):
        value = to_list(project_settings.get(self.name, global_settings.get(self.name, [])))

        if isinstance(self.settings[0], (list, tuple)):
            return self._insert(value, functor)

        return self._append(value, functor)

    def _append(self, value, functor):
        return {self.name: value + [s for s in self.settings if functor(s)]}

    def _insert(self, value, functor):
        for pos, klass in self.settings:
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
        return {self.name: value}

class GenericConfigurator(object):
    def __init__(self, settings, prefix):
        if not isinstance(settings, dict):
            self.application_settings = module_to_dict(settings)
        else:
            self.application_settings = settings

        self.prefix = prefix

    def prepare_settings(self, project_settings, options):
        from django.conf import global_settings
        from django.core.exceptions import ImproperlyConfigured

        result = {}

        global_settings = module_to_dict(global_settings)

        options = dict([(key.upper(), value) for key, value in options.iteritems()])
        work_options = options.copy()

        for name, value in self.application_settings.iteritems():
            global_value = project_settings.get(name, global_settings.get(name, None))

            if name.startswith(self.prefix):
                raw_name = name[len(self.prefix):]
            else:
                raw_name = name

            handler_name = "handle_%s" % raw_name.lower()
            handler = curry(getattr(self, handler_name, lambda x, options: True), options=options)

            if isinstance(value, Merge):
                result.update(value(project_settings, global_settings, handler))
            else:
                result[name] = value

        if work_options:
            result.update([("%s%s" % (self.prefix, key), value)
                            for key, value in work_options.iteritems()])

        return result

    def __call__(self, **options):
        import inspect

        outer_scope = inspect.stack()[1][0].f_locals

        outer_scope.update(self.merge_settings(outer_scope, **options))

    def merge_settings(self, project_settings, **options):
        return self.prepare_settings(project_settings, options)
