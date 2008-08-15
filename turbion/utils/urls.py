# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url( r'^captcha/',             "turbion.utils.captcha.views.image", name="captcha_image"),
    url( r'^status/',              "turbion.utils.views.status",        name="status"),
)