from django.core import urlresolvers
from django.conf import settings
from django.contrib.sites.models import Site

import urllib2
from urlparse import urlparse, urlsplit

from turbion.core.utils.urlfetch import fetch
from turbion.core.pingback import signals, utils, client
from turbion.core.pingback.models import Pingback
from turbion.models import Post

def ping(source_uri, target_uri, id):
    pingback, created = Pingback.objects.get_or_create(
        source_url=source_uri,
        target_url=target_uri,
        incoming=True
    )
    if not created:
        raise utils.PingError(0x0030)

    try:
        domain = Site.objects.get_current().domain
        scheme, server, path, query, fragment = urlsplit(target_uri)

        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            raise utils.PingError(0x0021)

        if post.get_absolute_url() != path + query:
            raise utils.PingError(0x0021)

        pingback.post = post

        try:
            doc = fetch(source_uri).content
        except (urllib2.HTTPError, urllib2.URLError), e:
            raise utils.PingError(0x0010)

        parser = utils.SourceParser(doc)
        title = pingback.title = parser.get_title()
        paragraph = pingback.paragraph = parser.get_paragraph(target_uri)

        status = pingback.status = 'Pingback from %s to %s registered. Keep the web talking! :-)' % (source_uri, target_uri)

        pingback.save()

        signals.pingback_recieved.send(
            sender=post.__class__,
            instance=post,
            pingback=pingback
        )

        return {
            "status": status,
            "source_title": title,
            "source_paragraph": paragraph,
            "source_uri": source_uri,
            "target_uri": target_uri,
            "model": model
        }
    except utils.PingError, e:
        pingback.status = e.code
        pingback.save()
        raise
