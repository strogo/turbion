# -*- coding: utf-8 -*-
import os

import turbion
from turbion.conf import Merge

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
    (None, 'turbion.dbtemplates.loader.load_template_source',),
]

TURBION_AUTHENTICATION_BACKENDS = [
    (None, 'turbion.openid.backend.OpenidBackend'),
    ('django.contrib.auth.backends.ModelBackend', "turbion.registration.backend.OnlyActiveBackend")
]

TURBION_LOCALE_PATHS = [
    os.path.join(os.path.dirname(turbion.__file__), "locale")
]

TURBION_INSTALLED_APPS          = Merge(TURBION_APPS, "INSTALLED_APPS")
TURBION_MIDDLEWARE_CLASSES      = Merge(TURBION_MIDDLEWARE_CLASSES, "MIDDLEWARE_CLASSES")
TURBION_CONTEXT_PROCESSORS      = Merge(TURBION_CONTEXT_PROCESSORS, "TEMPLATE_CONTEXT_PROCESSORS")
TURBION_TEMPLATE_LOADERS        = Merge(TURBION_TEMPLATE_LOADERS, "TEMPLATE_LOADERS")
TURBION_AUTHENTICATION_BACKENDS = Merge(TURBION_AUTHENTICATION_BACKENDS, "AUTHENTICATION_BACKENDS")
TURBION_LOCALE_PATHS            = Merge(TURBION_LOCALE_PATHS, "LOCALE_PATHS")

TURBION_BLOGS_MULTIPLE = False
TURBION_TITLE_PATTERN = '%(page)s | %(section)s | %(site)s'

TURBION_OPENID_STORE_ROOT = "/var/tmp/"

TURBION_BASE_UPLOAD_PATH = "upload/turbion/"

TURBION_POST_PERMALINK_PREFIX = ""

TURBION_USE_DJAPIAN = False

from turbion.pingback.settings import *
from turbion.openid.settings import *

# Djapian related
DJAPIAN_DATABASE_PATH = "djapian"
