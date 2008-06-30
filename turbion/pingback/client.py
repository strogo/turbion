# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
import xmlrpclib
import re

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from pantheon.utils.urlfetch import fetch

def search_link(content):
    match = re.search(r'<link rel="pingback" href="([^"]+)" ?/?>', content)
    return match and match.group(1)

def get_class( path ):
    if isinstance( path, basestring ):
        module, name = path.rsplit( ".", 1 )
        mod = __import__( module, {}, {}, [ "" ] )
        return getattr( mod, name )
    return path

def get_rpc_gateway( target_uri ):
    try:
        response = fetch( target_uri )
        return response.headers.get( 'X-Pingback', '') or search_link( response.content[ : 512 * 1024 ] )
    except (IOError, ValueError), e:
        print e
        return None

def call_ping( gateway, source_uri, target_uri ):
    try:
        server = xmlrpclib.ServerProxy( gateway, transport = get_class( settings.PINGBACK_TRANSPORT )() )
        q = server.pingback.ping( source_uri, target_uri )
        return q
    except xmlrpclib.Fault, e:
        return str( e )

def get_value( obj, name, default = None, args = [] ):
    try:
        attr = getattr( obj, name )

        if callable( attr ):
            attr = attr(*args)
        return attr
    except AttributeError:
        return default

def process_for_pingback( sender, instance, url, text ):
    from turbion.pingback.models import Outgoing
    from turbion.pingback import utils

    domain = Site.objects.get_current().domain

    ct = ContentType.objects.get_for_model( sender )

    local_uri = 'http://%s%s' % ( domain, url )

    for target_url in utils.parse_html_links( text, domain ):
        try:
            Outgoing.objects.get( target_uri = target_url,
                                    content_type = ct,
                                    object_id = instance.id,
                                    status = True )
            continue# do nothing if we just have pinged this url from this instance of model
        except Outgoing.DoesNotExist:
            pass

        if True:
            #make ping client
            gateway = get_rpc_gateway( target_url )
            
            if not gateway:
                continue

            status = call_ping(gateway, local_uri, target_url)
            print status
        #except TypeError, e:
        #    status = str( e )
        #    gateway = None

        out = Outgoing.objects.create( content_type = ct,
                                       object_id = instance.id,
                                       target_uri = target_url,
                                       rpcserver = gateway,
                                       status = status
                                    )
