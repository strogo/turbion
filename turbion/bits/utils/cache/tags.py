from inspect import getargspec

from django.template import TemplateSyntaxError, Node, Variable, generic_tag_compiler, Context
from django.utils.itercompat import is_iterable
from django.utils.functional import curry
from django.utils.encoding import smart_str
from django.conf import settings

from turbion.bits.utils.cache.utils import CacheWrapper

def cached_inclusion_tag(register, trigger, suffix, file_name, context_class=Context, takes_context=False):
    def _wrapper(func):
        decorated_function = getattr(func, "_decorated_function", func)
        func_name = decorated_function.__name__
        func_module = decorated_function.__module__

        base_name = func_module + "." + func_name

        params, xx, xxx, defaults = getargspec(func)
        if takes_context:
            if params[0] == 'context':
                params = params[1:]
            else:
                raise TemplateSyntaxError("Any tag function decorated with takes_context=True must have a first argument of 'context'")

        class CachedInclusionNode(Node):
            def __init__(self, vars_to_resolve):
                self.vars_to_resolve = map(Variable, vars_to_resolve)

            def render(self, context):
                resolved_vars = [var.resolve(context) for var in self.vars_to_resolve]

                if takes_context:
                    args = [context] + resolved_vars
                else:
                    args = resolved_vars

                def real_render(*args):
                    dict = func(*args)

                    if not getattr(self, 'nodelist', False):
                        from django.template.loader import get_template, select_template
                        if not isinstance(file_name, basestring) and is_iterable(file_name):
                            t = select_template(file_name)
                        else:
                            t = get_template(file_name)
                        self.nodelist = t.nodelist

                    result = self.nodelist.render(context_class(dict,
                            autoescape= context.autoescape))

                    return result

                w = CacheWrapper(
                        real_render,
                        trigger,
                        suffix,
                        base_name
                    )

                return w(*args)

        compile_func = curry(generic_tag_compiler, params, defaults, func_name, CachedInclusionNode)
        compile_func.__doc__ = func.__doc__
        register.tag(func_name, compile_func)
        return func
    return _wrapper
