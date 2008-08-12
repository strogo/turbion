# -*- coding: utf-8 -*-

try:
    from pytils import translit
    
    slugify = translit.slugify
except ImportError:
    from django.template import defaultfilters
    
    slugify = defaultfilters.slugify

