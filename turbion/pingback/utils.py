# -*- coding: utf-8 -*-
from django.conf import settings
#from django.contrib.sites.models import Site
from django.utils.html import strip_tags

from urlparse import urlsplit
from BeautifulSoup import BeautifulSoup


def parse_html_links( text, domain ):
    def is_external(external):
        path_e = urlsplit(external)[2]
        return path_e != domain

    soup = BeautifulSoup( text )
    #domain = Site.objects.get_current().domain

    links = []
    for a in soup.findAll('a'):
        href = a['href']

        if not href.startswith( "http://" ):
            href = "http://%s%s" % ( domain, href )
        if not is_external( href ):
            continue

        links.append( href )

    return links

class PingError( Exception ):
    def __init__( self, code ):
        self.code = code
        super( PingError, self ).__init__( "pingback.ping: error with code %s" % code )

class SourceParser( object ):
    def __init__( self, content ):
        self.soup = BeautifulSoup( content )

    def get_title(self):
        try:
            title = self.soup.find('title').contents[0]
            title = strip_tags(unicode(title))
        except AttributeError:
            return ""
        return title

    def get_paragraph( self, target_uri, max_length = None ):
        mylink = self.soup.find('a', href= target_uri )
        if not mylink:
            # The source URI does not contain a link to the target URI, and so cannot be used as a source.
            raise PingError( 0x0011 )

        content = unicode(mylink.findParent())
        mylink = unicode(mylink)
        i = content.index( mylink )
        content = strip_tags(content)
        max_length = max_length and max_length or settings.TURBION_PINGBACK_PARAGRAPH_LENGTH

        if len(content) > max_length:
            start = i - max_length/2
            if start < 0:
                start = 0
            end = i + len( mylink ) + max_length/2
            if end > len(content):
                end = len(content)
            content = content[start:end]
        mark = "[...]"
        return mark + content.strip() + mark
