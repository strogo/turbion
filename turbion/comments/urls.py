# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('turbion.comments.views',
    url( r'^(?P<comment_id>\d+)/delete/$',                     'delete', name = "comment_delete" ),
)
