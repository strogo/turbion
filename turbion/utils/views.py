# -*- coding: utf-8 -*-
from django import http
from django.core.urlresolvers import reverse

from turbion.utils.decorators import templated, titled

def status_redirect(request, title, section, message, next, button="Continue"):
    from django.utils.http import urlencode

    query = {"title"  : title,
            "section": section,
            "message": message,
            "next"   : next,
            "from"   : request.build_absolute_uri(),
            "button" : button,}

    return http.HttpResponseRedirect(reverse("turbion_status") + "?" + urlencode(query))

fields = ["title", "section", "message", "next", "button", "from"]

@templated("info_page.html")
@titled(page="{{title}}", section="{{section}}")
def status(request):
    data = dict([(key, value) for key, value in request.GET.iteritems() if key in fields])

    return data
