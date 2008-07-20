# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2008 Alexander Koshelev (daevaorn@gmail.com)
from django import http
from django.utils import simplejson

from turbion.roles.decorators import has_capability_for
from turbion.blogs.decorators import blog_view, post_view
from turbion.dashboard.schemas import SchemaSpot

def get_schema_or_404(name):
    try:
        return SchemaSpot.schemas[name]
    except KeyError:
        raise http.Http404

@blog_view
def source(request, blog, name):
    schema = get_schema_or_404(name)(blog)

    data = schema.get_data(request.GET)
    response = http.HttpResponse(mimetype="application/json")

    simplejson.dump(data, response)

    return response

@blog_view
def schema(request, blog, name):
    schema = get_schema_or_404(name)(blog)
