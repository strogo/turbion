# -*- coding: utf-8 -*-

TURBION_CONTEXT_PROCESSORS = [
    "turbion.options.context_processors.options_globals",
]

TURBION_APPS = [
    'pantheon.utils',
    'pantheon.postprocessing',
    'pantheon.supernovaforms',

    'dxapian',

    'turbion.tags',
    'turbion.comments',
    'turbion.blogs',
    'turbion.profiles',
    'turbion.feedback',
    'turbion.staticpages',

    'turbion.socialbookmarks',
    'turbion.pingback',
    'turbion.notifications',
    'turbion.gears',

    'turbion.dbtemplates',
    'turbion.roles',
    'turbion.options',
    'turbion.aliases',
    'turbion.openid',
    'turbion.registration',
    'turbion.dashboard',
    'turbion.assets'
]

TURBION_MIDDLEWARE_CLASSES = [
    (0,    'turbion.aliases.middleware.AliasesMiddleware', ),
    ('django.contrib.auth.middleware.AuthenticationMiddleware', 'turbion.profiles.middleware.AuthenticationMiddleware')
]

TURBION_TEMPLATE_LOADERS = [
    ( None, 'turbion.dbtemplates.loader.load_template_source', ),
]

TURBION_AUTHENTICATION_BACKENDS = [
    (None, 'turbion.openid.backend.OpenidBackend'),
    ('django.contrib.auth.backends.ModelBackend', "turbion.registration.backend.OnlyActiveBackend")
]

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

def append(source):
    @to_list
    def _func(value):
        return value + source
    return _func

def insert(source):
    @to_list
    def _func( value ):
        for pos, klass in source:
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
    return _func

patch_installed_apps     = append(TURBION_APPS)
patch_middleware_classes = insert(TURBION_MIDDLEWARE_CLASSES)
patch_context_processors = append(TURBION_CONTEXT_PROCESSORS)
patch_template_loaders   = insert(TURBION_TEMPLATE_LOADERS)
patch_authenticated_backends_loaders = insert(TURBION_AUTHENTICATION_BACKENDS)

TURBION_BLOGS_MULTIPLE = False
PANTHEON_TITLE_PATTERN = '%(page)s | %(section)s | %(site)s'

TURBION_OPENID_STORE_ROOT = "/var/tmp/"

TURBION_BASE_UPLOAD_PATH = "upload/turbion/"

TURBION_POST_PERMALINK_PREFIX = ""

from turbion.pingback.settings import *
