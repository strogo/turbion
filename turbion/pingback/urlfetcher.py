# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)

class UrlFetcher( object ):
    """
    Abstract url fetcher. Url fetcher is used by Client to
    retieve content form remote url
    """
    def get_header( self, name, default = None ):
        raise NotImplementedError
    
    def get_data( self, size ):
        raise NotImplementedError

class UrllibUrlFetcher( UrlFetcher ):
    """
    Url fetcher that uses urllib2 to retrive conent
    """
    def __init__(self, url):
        import urllib2
        urllib2.socket.setdefaulttimeout(10)
        
        self.url = url
        self.f = urllib2.urlopen( url )
        
    def get_header( self, name, default = None ):
        return self.f.info().get('X-Pingback', default)
    
    def get_data( self, size = None ):
        return self.f.read( size )