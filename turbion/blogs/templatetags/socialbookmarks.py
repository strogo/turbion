# -*- coding: utf-8 -*-
from django import template
from django.utils import http
from django.conf import settings
from django.contrib.sites.models import Site

register = template.Library()

installed = {
    "googlebookmarks": {
      "image": "turbion/images/socialbookmarks/google_bmarks.gif",
      "url": "http://www.google.com/bookmarks/mark?op=edit&bkmk=%(url)s&title=%(title)s",
    },
    "del.icio.us": {
      "image": "turbion/images/socialbookmarks/delicious.gif",
      "url": "http://del.icio.us/post?url=%(url)s&title=%(title)s",
    },
    "technorati": {
      "image": "turbion/images/socialbookmarks/technorati.gif",
      "url": "http://www.technorati.com/faves?add=%(url)s",
    },
    "memori": {
      "image": "turbion/images/socialbookmarks/memori.gif",
      "url": "http://memori.ru/link/?sm=1&u_data[url]=%(url)s&u_data[name]=%(title)s",
    },
    "bobrdobr": {
      "image": "turbion/images/socialbookmarks/bobrdobr.gif",
      "url": "http://bobrdobr.ru/addext.html?url=%(url)s&title=%(title)s",
    },
}

def fill_pattern(pattern, title, url, domain):
    return pattern % {
        "title": http.urlquote(title),
        "url": "http://%s%s" % (domain, http.urlquote(url))
    }

@register.inclusion_tag('turbion/blogs/include/socialbookmarks.html', takes_context=True)
def socialbookmarks_group(context, group, title, url):
    domain = Site.objects.get_current().domain

    return {
        "group" : [(name, fill_pattern(installed[name]["url"], title, url, domain), installed[name]["image"])
                        for name in [name.strip() for name in group.split(";") if name]],
        "title": title,
        "url": url,
        "domain": domain,
        "MEDIA_URL": settings.MEDIA_URL
    }
