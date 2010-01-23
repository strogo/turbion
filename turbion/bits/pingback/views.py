import urllib2
import socket
from urlparse import urlparse, urlsplit

from django import http
from django.contrib.sites.models import Site

from turbion import logger
from turbion.bits.utils.urlfetch import fetch
from turbion.bits.pingback import signals, utils, client
from turbion.bits.pingback.models import Pingback
from turbion.models import Post
from turbion.bits.utils import xmlrpc

gateway = xmlrpc.ServerGateway('pingback')

@gateway.connect
def ping(source_uri, target_uri, id):
    try:
        try:
            Pingback.objects.get(
                source_url=source_uri,
                target_url=target_uri,
                incoming=True
            )
            return 48
        except Pingback.DoesNotExist:
            pass

        domain = Site.objects.get_current().domain
        scheme, server, path, query, fragment = urlsplit(target_uri)

        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return 33

        if post.get_absolute_url() != path + query:
            return 33

        try:
            doc = fetch(source_uri).content
        except (urllib2.HTTPError, urllib2.URLError, socket.timeout), e:
            return 16

        parser = utils.SourceParser(doc)
        paragraph = parser.get_paragraph(target_uri)
        if paragraph is None:
            return 17

        pingback = Pingback.objects.create(
            source_url=source_uri,
            target_url=target_uri,
            incoming=True,
            title=parser.get_title(),
            paragraph=paragraph,
            status='Pingback from %s to %s registered. Keep the web talking! :-)' % (source_uri, target_uri),
            post=post,
            finished=True
        )

        signals.pingback_recieved.send(
            sender=post.__class__,
            instance=post,
            pingback=pingback
        )

        return pingback.status
    except Exception, e:
        logger.warning(str(e))

        return 0
