# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *

from turbion.blogs.utils import blog_url

urlpatterns = patterns( 'turbion.feedback.views',
    blog_url( r'^$',                          'index', name = "feedback" ),
    )
