# -*- coding: utf-8 -*-
import os

import turbion
from turbion.conf import Merge

TURBION_BASE_PATH = os.path.normpath(os.path.dirname(__file__))

TURBION_APPS = [
    'turbion',
]

TURBION_MIDDLEWARE_CLASSES = [
    ('django.contrib.auth.middleware.AuthenticationMiddleware',
     'turbion.core.profiles.middleware.AuthenticationMiddleware')
]

TURBION_AUTHENTICATION_BACKENDS = [
#    (None, 'turbion.openid.backend.OpenidBackend'),
    ('django.contrib.auth.backends.ModelBackend',
     "turbion.core.profiles.backend.OnlyActiveBackend")
]

TURBION_INSTALLED_APPS          = Merge(TURBION_APPS, "INSTALLED_APPS")
TURBION_MIDDLEWARE_CLASSES      = Merge(TURBION_MIDDLEWARE_CLASSES, "MIDDLEWARE_CLASSES")
TURBION_AUTHENTICATION_BACKENDS = Merge(TURBION_AUTHENTICATION_BACKENDS, "AUTHENTICATION_BACKENDS")

TURBION_BLOGS_MULTIPLE = False
TURBION_TITLE_PATTERN = '%(page)s | %(section)s | %(site)s'

TURBION_BASE_UPLOAD_PATH = "upload/turbion/"

TURBION_USE_DJAPIAN = False

TURBION_NOTIFACTIONS_FROM_EMAIL = "notifs@%(domain)s"
