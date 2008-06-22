# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django import template
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from urlparse import urljoin

register = template.Library()

@register.simple_tag
def generic_pingback_gateway( url, model ):
    url = reverse( url, args = ( model, ) )
    return '<link rel="pingback" href="%s" />' % urljoin( "http://" + Site.objects.get_current().domain, url )
    
@register.simple_tag
def pingback_gateway( model ):
    url = reverse( "turbion.pingback.views.gateway", args = ( model, ) )
    return '<link rel="pingback" href="%s" />' % urljoin( "http://" + Site.objects.get_current().domain, url )

def trackback_rdf( url, title, model, id ):
    return """<!--
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
             xmlns:dc="http://purl.org/dc/elements/1.1/"
             xmlns:trackback="http://madskills.com/public/xml/rss/module/trackback/">
    <rdf:Description
        rdf:about="%(url)s"
        dc:identifier="%(url)s"
        dc:title="%(title)s"
        trackback:ping="%(trackback_url)s" />
    </rdf:RDF>
    -->""" % { "title" : title,
               "url" : url,
               "trackback_url" : reverse( "turbion.pingback.views.trackback", kargs = { "model" :model,"id":id } ) }