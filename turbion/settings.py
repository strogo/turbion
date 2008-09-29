# -*- coding: utf-8 -*-

from turbion.conf import merge

TURBION_CONTEXT_PROCESSORS = [
    "turbion.options.context_processors.options_globals",
]

TURBION_APPS = [
    'turbion.utils.postprocessing',

    'djapian',

    'turbion.utils',
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

INSTALLED_APPS              = merge(TURBION_APPS)
MIDDLEWARE_CLASSES          = merge(TURBION_MIDDLEWARE_CLASSES)
TEMPLATE_CONTEXT_PROCESSORS = merge(TURBION_CONTEXT_PROCESSORS)
TEMPLATE_LOADERS            = merge(TURBION_TEMPLATE_LOADERS)
AUTHENTICATION_BACKENDS     = merge(TURBION_AUTHENTICATION_BACKENDS)

TURBION_BLOGS_MULTIPLE = False
TURBION_TITLE_PATTERN = '%(page)s | %(section)s | %(site)s'

TURBION_OPENID_STORE_ROOT = "/var/tmp/"

TURBION_BASE_UPLOAD_PATH = "upload/turbion/"

TURBION_POST_PERMALINK_PREFIX = ""

TURBION_USE_DJAPIAN = False

TURBION_HIDE_AUTH_APP = False

from turbion.pingback.settings import *
from turbion.openid.settings import *

# Djapian related
DJAPIAN_DATABASE_PATH = "djapian"
