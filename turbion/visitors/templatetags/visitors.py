# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007-2008 Alexander Koshelev (daevaorn@gmail.com)
from django import template
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.db.models import Q

from turbion.visitors.models import User

from datetime import datetime, timedelta


register = template.Library()

@register.simple_tag
def visitors_stats( template = "visitors/stats.html" ):
    bound  = datetime.now() - timedelta( minutes = 15 )

    gus    = list( User.registered.filter( last_visit__gte = bound ) )

    guests = User.guests.filter( last_visit__gte = bound )

    gus += [ g for g in guests if g.name ]

    ananymous = [ g for g in guests if not g.name ]

    return mark_safe( get_template( template ).render( Context( { "users" : gus,
                                                                  "ananymous" : len( ananymous ),
                                                                  "total_count" : len( gus ) + len( ananymous ) } ) ) )