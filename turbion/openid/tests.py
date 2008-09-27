# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import mail

import openid
from openid import fetchers

IDENTITY_FETCH = """<html>
<head>
<link rel="openid.server" href="http://www.livejournal.com/openid/server.bml" />
<meta http-equiv="X-XRDS-Location" content="http://daevaorn.livejournal.com/data/yadis" />
</head>
</html>
"""

YADIS_FETCH = """<?xml version="1.0" encoding="UTF-8"?>
<xrds:XRDS xmlns:xrds="xri://$xrds" xmlns="xri://$xrd*($v*2.0)"><XRD>
    <Service>
        <Type>http://openid.net/signon/1.0</Type>
        <URI>http://www.livejournal.com/openid/server.bml</URI>
    </Service>
</XRD></xrds:XRDS>
"""

REDIRECT_URL_DATA = "janrain_nonce=2008-06-29T14%3A10%3A21ZbwPCu5&openid1_claimed_id=http%3A%2F%2Fdaevaorn.livejournal.com%2F&openid.mode=id_res&openid.identity=http://daevaorn.livejournal.com/&openid.return_to=http://testserver/openid/authenticate/%3Fjanrain_nonce%3D2008-06-29T14%253A10%253A21ZbwPCu5%26openid1_claimed_id%3Dhttp%253A%252F%252Fdaevaorn.livejournal.com%252F&openid.assoc_handle=1214747759:WUK4pAAKCpJ2zFgJgeqH:0644328dda&openid.signed=mode,identity,return_to&openid.sig=rC4gk/vkyAXXL%2BEAnXW5j5uIXs4%3D"

class TestFetcher( fetchers.Urllib2Fetcher ):
    mapped = { "http://daevaorn.livejournal.com/" : ( 200, {}, IDENTITY_FETCH ),
               "http://daevaorn.livejournal.com/data/yadis" : ( 200, {},  YADIS_FETCH ),
             }

    def fetch( self, url, body=None, headers=None ):
        print "Fetching: ", url
        for mapped_url, data in self.mapped.iteritems():
            if url.startswith( mapped_url ):
                return fetchers.HTTPResponse( final_url = url,
                                              headers=data[1],
                                              body = data[2],
                                              status = data[0] )
        return super( TestFetcher, self ).fetch( url, body, headers)

fetchers.setDefaultFetcher(TestFetcher())

class OpenidLoginTest( TestCase ):
    def test_submit_feedback(self):
        data = { "openid" : "http://daevaorn.livejournal.com" }
        response = self.client.post( reverse( "openid_login" ), data = data )

        self.assertEqual( response.status_code, 302 )

    def test_authentication( self ):
        self.test_submit_feedback()
        response = self.client.post( reverse( "openid_authenticate" ),
                                    QUERY_STRING = REDIRECT_URL_DATA )
