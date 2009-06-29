from django.conf.urls.defaults import *

urlpatterns = patterns( 'turbion.bits.profiles.views',
    url(r'^(?P<profile_id>\d+)/$',    'profile',      name="turbion_profile"),
    url(r'^edit/$',                   'edit_profile', name="turbion_profile_edit"),
)
