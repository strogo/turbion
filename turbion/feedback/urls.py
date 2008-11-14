# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('turbion.feedback.views',
    url(r'^$',                          'index', name="turbion_feedback"),
)
