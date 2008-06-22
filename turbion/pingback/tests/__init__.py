# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from turbion.pingback import client, models, utils
from turbion.pingback.urlfetcher import UrlFetcher

from turbion.pingback.tests.client import TestTransport, TestClientUrlFetcher

from django.conf import settings

settings.PINGBACK_URLFETCHER = TestClientUrlFetcher
settings.PINGBACK_TRANSPORT = TestTransport

import xmlrpclib
from urlparse import urlsplit

class UrlsParseTestCase( TestCase ):
    def setUp(self):
        site = Site.objects.get_current()
        site.domain = "foobar.com"
        site.save()
        
        self.test_text = """<p>
            <a href="http://example.com/">a</a>
            <a href="http://foobar.com/">fff</a>
            <a href='http://test.ru/'>b</a>
            Some text here
            <a href="http://some-url.org/">c</a>
        </p>
        """
    
    def tearDown(self):
        pass
    
    def test_findlinks(self):
        links = utils.parse_html_links( self.test_text, "foobar.com" )
        
        self.assertEqual( len( links ), 4 )
        
        self.assertEqual( links, [ "http://example.com/", "http://foobar.com/", 
                                   "http://test.ru/", "http://some-url.org/" ] )

class ContentParseTestCase( TestCase ):
    def setUp(self):
        self.test_text = """"
        <html>
        <head>
            <title>Test Title</title>
        </head>
        <body>
            <p>
                Foo <a href="http://foobar.com/">foobar</a>Bar
            </p>
        </doby>
        </html>
        
        """
        self.parser = utils.SourceParser( self.test_text )
    
    def test_title(self):
        self.assertEqual( self.parser.get_title(), "Test Title" )
        
    def test_paragraph( self ):
        self.assertEqual( self.parser.get_paragraph("http://foobar.com/"), "[...]Foo foobarBar[...]" )

TITLE = ""
PARAGRAPH = "Вот параграф со ссылкой на пост с длинной строчкой"
TEXT = """<p>Вот первый параграф</p>

<p>Вот параграф со ссылкой <a href="%(target_url)s">на пост</a> с длинной строчкой</p>

<p>Третий параграф</p>
"""

class TestPing( TestCase ):
    fixtures = ["test/auth", "test/pingback"]
    
    def setUp(self):
        settings.PINGBACK_URLFETCHER.client = self.client
        settings.PINGBACK_TRANSPORT.client = self.client
        
        site = Site.objects.get_current()
        site.domain = "to.com"
        site.save()
        
        from turbion.blogs.models import Blog, Post
        blog = Blog.objects.all()[0]
        post = Post.objects.create( blog = blog, title="test", text="pingback post test", slug="test", draft = False )
        
        self.post = post
        
        self.TARGET_URI = "http://to.com%s" % post.get_absolute_url()
        global TEXT
        TEXT = TEXT % { "target_url" : self.TARGET_URI } 
        
        new_post = Post.objects.create( blog = blog, title = "test_post", slug="test_post", text=TEXT, draft = False )
        self.new_post = new_post
        
        self.SOURCE_URI = "http://from.com%s" % new_post.get_absolute_url()

    def t1est_outgoing(self):
        from turbion.pingback.models import Outgoing
        
        self.assertEqual( Outgoing.objects.count(), 1 )
        
        out = Outgoing.objects.get()
        self.assertEqual( out.object, self.post )
        self.assertEqual( out.url, self.TARGET_URI )
        
    def t1est_incoming(self):
        from turbion.pingback.models import Incoming
        
        self.assertEqual( Incoming.objects.count(), 1 )
        inc = Incoming.objects.get()
        
        self.assertEqual( inc.object, self.new_post )
        self.assertEqual( inc.title, TITLE )
        self.assertEqual( inc.content, PARAGRAPH )
        
        self.assertEqual( inc.source_uri, self.SOURCE_URI )

def get_test_post():
    from turbion.blogs.models import Blog, Post
    blog = Blog.objects.filter()[0]
    post = Post.objects.create( blog = blog, title="test", text="pingback post test", slug="test", draft = False )
    return post        
  
class TextTrackback( TestCase ):
    fixtures = ["test/auth", "test/pingback"]
    
    def setUp(self):
        self.post = get_test_post()
        self.trackback_url = reverse( "turbion.pingback.views.trackback",
                                      kwargs = { "model" : "blogs.post","id":self.post.id } )
        
    def test_good_request(self):
        response = self.client.post( self.trackback_url, { "url" : "http://foobar.com/entry/foo/" } )
        self.assertEqual( response.status_code, 200 )
        
        self.assertEqual( models.Incoming.objects.count(), 1 )
        incoming = models.Incoming.objects.get()
        
        self.assertEqual( incoming.status, "done" )
        
        self.assertEqual( incoming.target_url, "http://testserver" + self.trackback_url )
        self.assertEqual( incoming.source_url, "http://foobar.com/entry/foo/" )
        