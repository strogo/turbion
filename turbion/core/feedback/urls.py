# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('turbion.core.feedback.views',
    url(r'^$', 'index', name="turbion_feedback"),
)
