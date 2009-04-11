from django.conf.urls.defaults import *

urlpatterns = patterns('turbion.contrib.openid.views',
    url(r'^xrds/$',                  'xrds',                       name="turbion_openid_xrds"),

    url(r'^login/$',                 'authorization.login',        name="turbion_openid_login"),
    url(r'^authenticate/$',          'authorization.authenticate', name="turbion_openid_authenticate"),

    url(r'^server/endpoint/$',       'server.endpoint',    name="turbion_openid_endpoint"),
    url(r'^server/decide/$',         'server.decide',      name="turbion_openid_decide"),
)
