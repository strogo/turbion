# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007-2008 Alexander Koshelev (daevaorn@gmail.com)
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.dispatch import dispatcher

from django.contrib.sites.models import Site

import urllib2
from urlparse import urlparse, urlsplit

from turbion.pingback import signals
from turbion.pingback import client
from turbion.pingback.models import Incoming
from turbion.pingback import utils

def resolve_url( url ):
    resolver = urlresolvers.RegexURLResolver(r'^/', settings.ROOT_URLCONF)
    try:
        func, args, kwargs = resolver.resolve( url )
        return args, kwargs
    except urlresolvers.Resolver404:
        # The specified target URI does not exist.
        raise utils.PingError( 0x0020 )

def resolve_model( model ):
    app_label, model_name = model.split( '.',1 )
    try: 
        ct = ContentType.objects.get( app_label = app_label, model = model_name )
    except ContentType.DoesNotExist:
        raise utils.PingError( 0x0021 )    
        
    return ct.model_class()

def resolve_object( model, args, kwargs ):
    try:
        obj = model.get_for_pingback( *args, **kwargs )
    except AttributeError:
        raise utils.PingError( 0x0021 )
    return obj

def ping( source_uri, target_uri, model ):
    incoming, created = Incoming.objects.get_or_create( source_url = source_uri,
                                               target_url = target_uri )
    if not created:
        raise utils.PingError( 0x0030 )
    
    try:
        path = urlparse( target_uri )[ 2 ]
    
        domain = Site.objects.get_current().domain
        scheme, server, path, query, fragment = urlsplit(target_uri)
    
        if not server.split(':')[0] == domain.split(':')[0]:
            # The specified target URI cannot be used as a target.
            raise utils.PingError( 0x0021 )
    
        args, kwargs = resolve_url( path )        
        model = resolve_model( model )

        obj = resolve_object( model, args, kwargs )
        
        incoming.object = obj
    
        #now try to recieve source url and parse content
        try:
            fetcher = client.get_class(settings.PINGBACK_URLFETCHER)( source_uri )
            doc =  fetcher.get_data()
        except (urllib2.HTTPError, urllib2.URLError), e:
            # The source URI does not exist.
            raise utils.PingError( 0x0010 )
    
        parser = utils.SourceParser( doc )
        title = incoming.title = parser.get_title()
        paragraph = incoming.paragraph = parser.get_paragraph( target_uri )
        
        status = incoming.status = 'Pingback from %s to %s registered. Keep the web talking! :-)' % ( source_uri, target_uri )
        
        incoming.save()
        
        dispatcher.send(signal=signals.pingback_recieved, sender=obj.__class__,
                        instance=obj, incoming=incoming)
            
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