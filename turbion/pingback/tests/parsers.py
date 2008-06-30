# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.test import TestCase
from django.contrib.sites.models import Site

from turbion.pingback import utils

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
