# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from turbion.pingback.transport import XmlRpcTransport
from turbion.pingback.urlfetcher import UrlFetcher
from urlparse import urlsplit

class TestConnection( object ):
    def __init__(self, client, host ):
        self.host = host
        self.url = None
        
        self.client = client
        self.headers = {}
        self.body = None
        
    def set_debuglevel(self,val):
        pass
    
    def putrequest(self,val,handler):
        self.method = val
        self.url = handler
    
    def putheader(self,key, value ):
        self.headers[ key.upper() ] = value
    
    def endheaders(self):
        pass
    
    def getfile(self):
        from StringIO import StringIO
        return StringIO( self.response.content )
    
    def getreply(self):
        self._response = None
        return self.response.status_code, "", self.response.items()
        #errcode, errmsg, headers 
        
    def send( self, body ):
        self.body = body
    
    def _get_response(self):
        if not getattr( self, "_response", False ):
            self._response = self.client.post( self.url,
                                               data = self.body,
                                               content_type = self.headers.get( "CONTENT-TYPE", "text/xml" ),
                                               **self.headers )
        return self._response
    response = property( _get_response )
    
class TestTransport( XmlRpcTransport, object ):
    def __init__(self, client = None ):
        if client:
            self.client = client
        super( TestTransport, self ).__init__()
        
    def make_connection(self, host):
        return TestConnection( self.client, host )
    
class TestClientUrlFetcher( UrlFetcher ):
    def __init__( self, url ):
        self.url = url
        url = urlsplit( self.url )[2]
        self.response = self.client.get( url )
        
    def get_data(self, size=None):
        return self.response.content[:size]
    
    def get_header(self, name, default = None ):
        return self.response.get( name, default )