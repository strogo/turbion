# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *

urlpatterns = patterns('turbion.comments.views',
    url( r'^(?P<comment_id>\d+)/delete/$',                     'delete', name = "comment_delete" ),
)
