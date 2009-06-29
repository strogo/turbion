from django.conf.urls.defaults import *

urlpatterns = patterns('turbion.core.openid.views',
    url(r'^xrds/$',                  'xrds',               name="turbion_openid_xrds"),

    url(r'^login/$',                 'auth.login',         name="turbion_openid_login"),
    url(r'^authenticate/$',          'auth.authenticate',  name="turbion_openid_authenticate"),

    url(r'^server/endpoint/$',       'server.endpoint',    name="turbion_openid_endpoint"),
    url(r'^server/decide/$',         'server.decide',      name="turbion_openid_decide"),
)
