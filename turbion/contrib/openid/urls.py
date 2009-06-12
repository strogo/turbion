from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('turbion.contrib.openid.views',
    url(r'^xrds/$',                  'xrds',               name="turbion_openid_xrds"),

    url(r'^login/$',                 'auth.login',         name="turbion_openid_login"),
    url(r'^authenticate/$',          'auth.authenticate',  name="turbion_openid_authenticate"),

    url(r'^server/endpoint/$',       'server.endpoint',    name="turbion_openid_endpoint"),
    url(r'^server/decide/$',         'server.decide',      name="turbion_openid_decide"),
)

if 'turbion.contrib.openid.whitelist' in settings.INSTALLED_APPS:
    from turbion.core.profiles.models import Profile

    queryset = Profile.objects.filter(trusted=True).exclude(openid='').values_list('openid', flat=True)

    urlpatterns += patterns('turbion.contrib.openid.whitelist.views',
        url(r'^whitelist/$', 'whitelist', {'queryset': queryset}, name='turbion_whitelist')
    )
