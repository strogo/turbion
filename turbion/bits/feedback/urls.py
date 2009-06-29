from django.conf.urls.defaults import *

urlpatterns = patterns('turbion.bits.feedback.views',
    url(r'^$', 'index', name="turbion_feedback"),
)
