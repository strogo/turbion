from django import http
from django.shortcuts import *
from django.conf import settings

from turbion.utils import xmlrpc
from turbion.pingback import utils, server, signals, models

gateway = xmlrpc.ServerGateway("pingback")

@gateway.connect
def ping(source_uri, target_uri, model_id, id):
    try:
        res = server.ping(source_uri, target_uri, model_id, id)
        return res["status"]
    except utils.PingError, e:
        return e.code
