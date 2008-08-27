# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django import http

from turbion.profiles.models import Profile
from turbion.notifications.models import Event
from turbion.notifications.eventdescriptor import EventSpot
from turbion.utils.views import status_redirect

def unsubscribe(request, user_id, event_id):
    user  = get_object_or_404(Profile, pk=user_id)
    event = get_object_or_404(Event, pk=event_id)

    try:
        desc = EventSpot.descriptors[event.descriptor]
    except KeyError:
        raise http.Http404

    hash = desc.get_user_hash(user)

    if not "code" in request.GET or request.GET["code"] != hash:
        raise http.Http404

    if "connection_ct_id" in request.GET and "connection_id" in request.GET:
        connection_ct = get_object_or_404(ContentType, pk=request.GET["connection_ct_id"])
        connection_id = request.GET["connection_id"]

        obj = connection_ct.get_object_for_this_type(pk=connection_id)
    else:
        obj = None

    desc.unsubscribe(user, obj)

    return status_redirect(request,
                    title  =u"Отписка",
                    section=u"Оповещения",
                    message=u'Вы отписаны от уведомлений в теме "%s"' % desc.name,
                    next   ="/" )
