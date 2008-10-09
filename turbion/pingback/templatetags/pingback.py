# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from urlparse import urljoin

register = template.Library()

@register.simple_tag
def pingback_gateway(obj):
    ct = ContentType.objects.get_for_model(obj.__class__)
    url = reverse("pingback_gateway", args=(ct.id, obj._get_pk_val()))

    return '<link rel="pingback" href="%s" />' % urljoin("http://" + Site.objects.get_current().domain, url)

def trackback_rdf( url, title, obj ):
    ct = ContentType.objects.get_for_model( obj.__class__ )

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
               "trackback_url" : reverse( "turbion.pingback.views.trackback", kargs = { "model_id": ct.id,
                                                                                        "id" : obj._get_pk_val() } ) }
