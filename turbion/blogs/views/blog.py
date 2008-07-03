# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps.views import sitemap as django_sitemap
from django.contrib.syndication import feeds
from django import http
from django.contrib.sites.models import Site
from django.core import urlresolvers
from django.template import loader

from turbion.blogs.decorators import blog_view, titled
from turbion.blogs.models import Blog, Post, Comment

from pantheon.utils.decorators import paged, templated
from pantheon.utils.paging import paginate

@blog_view
def sitemap( request, blog, sitemaps ):
    return django_sitemap( request, sitemaps = dict( [ ( k, s( blog ) ) for k, s in sitemaps.iteritems() ] ) )

def index_sitemap( request, sitemaps ):
    current_site = Site.objects.get_current()
    sites = []
    protocol = request.is_secure() and 'https' or 'http'
    
    for slug in Blog.objects.all().values_list( "slug", flat = True ):
        sitemap_url = urlresolvers.reverse( 'blog_sitemap', kwargs={'blog': slug})
        sites.append('%s://%s%s' % (protocol, current_site.domain, sitemap_url))
        
        sitemap_url = urlresolvers.reverse( 'page_sitemap', kwargs={'blog': slug})
        sites.append('%s://%s%s' % (protocol, current_site.domain, sitemap_url))
    
    xml = loader.render_to_string('sitemap_index.xml', {'sitemaps': sites})
    return http.HttpResponse(xml, mimetype='application/xml')

@blog_view
def feed( request, blog, url, feed_dict ):
    if not feed_dict:
        raise http.Http404, "No feeds are registered."

    try:
        slug, param = url.split('/', 1)
    except ValueError:
        slug, param = url, ''

    try:
        f = feed_dict[slug]
    except KeyError:
        raise http.Http404, "Slug %r isn't registered." % slug

    try:
        feedgen = f( blog, slug, request).get_feed(param)
    except feeds.FeedDoesNotExist:
        raise http.Http404, "Invalid feed parameters. Slug %r is valid, but other parameters, or lack thereof, are not." % slug

    response = http.HttpResponse(mimetype=feedgen.mime_type)
    feedgen.write(response, 'utf-8')
    return response

@templated( 'turbion/blogs/404.html' )
@titled( page = u'Страница не найден' )
def handler404( request ):
    return { }

@templated( 'turbion/blogs/500.html' )
@titled( page = u'Страница не найден' )
def handler500( request ):
    return { }
