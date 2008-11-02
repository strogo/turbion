# -*- coding: utf-8 -*-
from django.core import urlresolvers
from django.conf import settings
from django.contrib.sites.models import Site

import urllib2
from urlparse import urlparse, urlsplit

from turbion.utils.urlfetch import fetch
from turbion.pingback import signals
from turbion.pingback import client
from turbion.pingback.models import Incoming
from turbion.pingback import utils
from turbion.utils.descriptor import to_object

def resolve_model(model_id):
    try:
        dscr = to_object(model_id)
    except ValueError:
        raise utils.PingError(0x0021)

    return dscr

def resolve_object(model, id):
    try:
        obj = model._default_manager.get(pk=id)
    except ( model.DoesNotExist, ):
        raise utils.PingError( 0x0021 )
    return obj

def ping(source_uri, target_uri, model_id, id):
    incoming, created = Incoming.objects.get_or_create(
                                    source_url=source_uri,
                                    target_url=target_uri
                            )
    if not created:
        raise utils.PingError( 0x0030 )

    try:
        domain = Site.objects.get_current().domain
        scheme, server, path, query, fragment = urlsplit(target_uri)

        model = resolve_model( model_id )

        obj = resolve_object( model, id )
        if obj.get_absolute_url() != path + query:
            # The specified target URI cannot be used as a target.
            raise utils.PingError( 0x0021 )

        incoming.object = obj

        #now try to recieve source url and parse content
        try:
            doc =  fetch( source_uri ).content
        except (urllib2.HTTPError, urllib2.URLError), e:
            # The source URI does not exist.
            raise utils.PingError( 0x0010 )

        parser = utils.SourceParser( doc )
        title = incoming.title = parser.get_title()
        paragraph = incoming.paragraph = parser.get_paragraph(target_uri)

        status = incoming.status = 'Pingback from %s to %s registered. Keep the web talking! :-)' % ( source_uri, target_uri )

        incoming.save()

        signals.pingback_recieved.send(
                    sender=obj.__class__,
                    instance=obj,
                    incoming=incoming
            )

        return { "status" : status,
                 "source_title": title,
                 "source_paragraph" : paragraph,
                 "source_uri" : source_uri,
                 "target_uri" : target_uri,
                 "model" : model
            }
    except utils.PingError, e:
        incoming.status = e.code
        incoming.save()
        raise
