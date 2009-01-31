# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('turbion.core.comments.views',
    url(r'^(?P<comment_id>\d+)/delete/$',       'delete', name="turbion_comment_delete"),
)
