from django.conf.urls.defaults import *

urlpatterns = patterns('turbion.bits.markup.views',
    url(r'^preview/$',           'preview',           name='markup_preview'),
)
