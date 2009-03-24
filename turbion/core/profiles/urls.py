from django.conf.urls.defaults import *

urlpatterns = patterns( 'turbion.core.profiles.views',
    url(r'^(?P<profile_id>\d+)/$',       'profile',      name="turbion_profile"),
    url(r'^(?P<profile_id>\d+)/edit/$',  'edit_profile', name="turbion_profile_edit"),
)
