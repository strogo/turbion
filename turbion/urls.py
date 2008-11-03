# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings

from turbion.blogs.utils import blog_url
from turbion import admin

urlpatterns = patterns('',
    url(r'^profile/',                      include('turbion.profiles.urls')),
    url(r'^openid/',                       include('turbion.openid.urls')),
    url(r'^pingback/',                     include('turbion.pingback.urls')),
    url(r'^notifications/',                include('turbion.notifications.urls')),
    url(r'^roles/',                        include('turbion.roles.urls')),
    url(r'^comments/',                     include('turbion.comments.urls')),
    url(r'^gears/',                        include('turbion.gears.urls')),
    url(r'^registration/',                 include('turbion.registration.urls')),
    url(r'^dashboard/raw/(.*)',            admin.site.root, name="admin_root"),
    url(r'^dashboard/',                    include('turbion.dashboard.urls')),
    url(r'^utils/',                        include('turbion.utils.urls')),

    blog_url(r'',                          include('turbion.blogs.urls')),
    blog_url(r'pages/',                    include('turbion.staticpages.urls')),
    blog_url(r'feedback/',                 include('turbion.feedback.urls')),
)

if settings.TURBION_BLOGS_MULTIPLE:
    urlpatterns += patterns('',
                    url(r'^sitemap.xml$',
                        'turbion.blogs.views.blog.index_sitemap',
                        name="global_blog_sitemap"
                        )
                )
