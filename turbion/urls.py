# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings

from turbion.core.blogs.utils import blog_url
from turbion import admin

urlpatterns = patterns('',
    url(r'^comments/',            include('turbion.core.comments.urls')),
    url(r'^dashboard/(.*)',       admin.site.root, name="turbion_admin_root"),
    url(r'^utils/',               include('turbion.core.utils.urls')),
    url(r'^profile/',             include('turbion.core.profiles.urls')),
    url(r'^notifications/',       include('turbion.core.notifications.urls')),

    blog_url(r'',                 include('turbion.core.blogs.urls')),
    blog_url(r'pages/',           include('turbion.core.staticpages.urls')),
    blog_url(r'feedback/',        include('turbion.core.feedback.urls')),

    url(r'^sitemap.xml$',        'turbion.core.blogs.views.blog.index_sitemap', name="turbion_global_blog_sitemap"),
)

urlpatterns1 = patterns('',
    url(r'^openid/',              include('turbion.openid.urls')),
    url(r'^pingback/',            include('turbion.pingback.urls')),
    url(r'^gears/',               include('turbion.gears.urls')),
    url(r'^registration/',        include('turbion.registration.urls')),
)

from turbion import loading

loading.admins()
loading.connectors()
