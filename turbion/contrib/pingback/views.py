# -*- coding: utf-8 -*-
from django import http
from django.db.models import ObjectDoesNotExist
from django.shortcuts import *
from django.conf import settings

from turbion.utils import xmlrpc
from turbion.pingback import utils, server, signals, models

from datetime import datetime

gateway = xmlrpc.ServerGateway("pingback")

@gateway.connect
def ping(source_uri, target_uri, model_id, id):
    try:
        res = server.ping(source_uri, target_uri, model_id, id)
        return res["status"]
    except utils.PingError, e:
        return e.code

def trackback(request, model, id):
    if request.POST:
        message = "done"
        error = 0

        target_url = request.build_absolute_uri()

        incoming = models.Incoming(target_url=target_url)

        try:
            title = request.POST.get("title", "")
            if title:
                incoming.title = title

            url = request.POST["url"]
            incoming.source_url = url

            excerpt = request.POST.get("excerpt", "")
            blog_name = request.POST.get("blog_name", "")
            incoming.paragraph = excerpt + "\n\n" + blog_name

            model = server.resolve_model(model)
            object = model.objects.get(pk=id)
            incoming.object = object

            incoming.save()
            signals.trackback_recieved.send(
                        sender=object.__class__,
                        instance=object,
                        incoming=incoming
                )
        except KeyError:
            error = 1
            message = "Source url is needed"
            incoming.source_url = request.META["REMOTE_ADDR"] + "%s" % datetime.now()
        except (utils.PingError, ObjectDoesNotExist):
            error = 1
            message = "Illegal trackback url"

        incoming.status = message
        incoming.save()

        response = render_to_response( "pingback/trackback.html", {"encoding": settings.DEFAULT_CHARSET,
                                                                   "error": error,
                                                                   "message": message})
        response["CONTENT_TYPE"] = "text/xml; charset=%s" % settings.DEFAULT_CHARSET
        return response
    else:
        return http.Http404
