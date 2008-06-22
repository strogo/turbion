# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django import http

from turbion.visitors.models import User
from turbion.notifications.models import Event
from turbion.notifications.eventdescriptor import EventSpot

from pantheon.utils.views import info_page

def unsubscribe( request, user_id, event_id ):
    user  = get_object_or_404( User,  pk = user_id )
    event = get_object_or_404( Event, pk = event_id )

    try:
        desc = EventSpot.descriptors[ event.descriptor ]
    except KeyError:
        raise http.Http404

    hash = desc.get_user_hash( user )

    if not "code" in request.GET or request.GET[ "code" ] != hash:
        raise http.Http404

    if "connection_ct_id" in request.GET and "connection_id" in request.GET:
        connection_ct = get_object_or_404( ContentType, pk = request.GET[ "connection_ct_id" ] )
        connection_id = request.GET[ "connection_id" ]

        obj = connection_ct.get_object_for_this_type( pk = connection_id )
    else:
        obj = None

    desc.unsubscribe( user, obj )

    return info_page( request,
                      title   = u"Отписка",
                      section = u"Оповещения",
                      message = u'Вы отписаны от уведомлений в теме "%s"' % desc.name,
                      next    = "/" )
