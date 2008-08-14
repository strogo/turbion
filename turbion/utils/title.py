# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.utils.encoding import smart_unicode
from django.conf import settings

def gen_title( bits, pattern = None ):
    domain = Site.objects.get_current().domain

    pattern = settings.PANTHEON_TITLE_PATTERN

    defaults = { "page" : u"Страница", "section":u"Раздел","site":domain }
    defaults.update( bits )

    return smart_unicode( pattern ) % defaults
