# -*- coding: utf-8 -*-
from inspect import getargspec

from django.template import TemplateSyntaxError, Node, Variable, generic_tag_compiler
from django.utils.functional import curry

from turbion.core.utils.loading import get_module_attrs

__path__.extend(get_module_attrs("turbion.core.utils.markup", "templatetags")["__path__"])

def simple_tag_with_request( register ):
    def _wrapper( func ):
        decorated_function = getattr(func, "_decorated_function", func)
        func_name = decorated_function.__name__

        params, xx, xxx, defaults = getargspec(func)
        if params[0] == 'request':
            params = params[1:]
        else:
            raise TemplateSyntaxError("Any tag function must have a first argument of 'request'")

        class RequestNode(Node):
            def __init__(self, vars_to_resolve):
                self.vars_to_resolve = map(Variable, vars_to_resolve)

            def render(self, context):
                resolved_vars = [var.resolve(context) for var in self.vars_to_resolve]
                args = [context["request"]] + resolved_vars
                value = func(*args)
                return value

        compile_func = curry(generic_tag_compiler, params, defaults, func_name, RequestNode)
        compile_func.__doc__ = func.__doc__
        register.tag( func_name, compile_func)
        return func
    return _wrapper
