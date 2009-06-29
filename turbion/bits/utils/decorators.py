from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.template import Context, Template
from django.utils.encoding import smart_unicode
from django import http
from django.template.context import get_standard_processors

from turbion.bits.utils.title import gen_title

__all__ = ["status", "paged", "templated", "titled", "special_titled"]

class LocalRequestContext(Context):
    def __init__(self, request, dict=None, processors=None):
        Context.__init__(self, dict)
        if processors is None:
            processors = ()
        else:
            processors = tuple(processors)

        for processor in get_standard_processors():
            self.update(processor(request))

        for processor in processors:
            self.update(processor(request, self))

class PageMeta(object):
    def __init__(self, request, context, template=None):
        self.request = request
        self.context = context
        self.template = template
        self.processors = []
        self.status_code = 200

    def __getitem__(self, name):
        return self.context[name]

    def add_processor(self, processor):
        self.processors.append(processor)

    def __setitem__(self, name, value):
        self.context[name] = value

    def get(self, name, default=None):
        return self.context.get(name, default)

    def update(self, data):
        self.content.update(data)

    def render_to_response(self, template=None):
        context = LocalRequestContext(self.request,
                                  self.context,
                                  self.processors
                                )
        if not template:
            template = self.template
        response = render_to_response(template,
                                  context_instance=context
                )
        response.status_code = self.status_code
        return response

def ensure_meta(request, response):
    if isinstance(response, (tuple, list)):
        return PageMeta( request=request,
                        context =response[0],
                        template=response[1])
    elif isinstance(response, dict):
        return PageMeta(request=request,
                        context=response)
    return response

def status(code=200):
    def _wrapper(func):
        def _decor(request, *args, **kwargs):
            meta = ensure_meta(request, func(request, *args, **kwargs))
            if isinstance(meta, PageMeta):
                meta.status_code = code
            return meta
        _decor.__doc__  = func.__doc__
        _decor.__dict__ = func.__dict__
        _decor.__name__ = func.__name__
        return _decor
    return _wrapper

def templated(template=None):
    def _wrapper(func):
        def _decor(request, *args, **kwargs):
            meta = ensure_meta(request, func(request, *args, **kwargs))
            if isinstance(meta, PageMeta):
                return meta.render_to_response(template)
            return meta
        _decor.__doc__  = func.__doc__
        _decor.__dict__ = func.__dict__
        _decor.__name__ = func.__name__
        return _decor
    return _wrapper

def titled(**bits):
    def _wrapper(func):
        def _decor(request, *args, **kwargs):
            def _title_processor(request, context):
                defaults = {"site" : request.META['SERVER_NAME']}
                defaults.update(bits)
                pattern = gen_title(defaults)

                template = Template(pattern)
                title = template.render(context)
                return {"page_title": title}

            meta = ensure_meta(request, func(request, *args, **kwargs))
            if isinstance(meta, PageMeta):
                meta.add_processor(_title_processor)
            return meta
        _decor.__doc__  = func.__doc__
        _decor.__dict__ = func.__dict__
        _decor.__name__ = func.__name__
        return _decor
    return _wrapper

def special_titled(**default):
    def another_wrapper(**bits):
        my_default = default.copy()
        my_default.update(bits)
        return titled(**my_default)
    return another_wrapper

def paged(view_func):
    def _decor(request, *args, **kwargs):
        request.page = request.GET.get('page', 1)
        return view_func(request, *args, **kwargs)
    _decor.__doc__  = view_func.__doc__
    _decor.__dict__ = view_func.__dict__
    _decor.__name__ = view_func.__name__
    return _decor
