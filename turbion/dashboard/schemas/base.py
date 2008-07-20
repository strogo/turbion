# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.utils.encoding import smart_str

class SchemaSpot(type):
    def __new__(cls, name, bases, attrs):
        try:
            Schema
        except NameError:
            cls.schemas = {}

            return super(SchemaSpot,cls).__new__(cls, name, bases, attrs)

        model = attrs["model"]
        if not "fields" in attrs:
            attrs["fields"] = [field.name for field in model._meta.fields]
        schema_name = attrs.get("name", name)

        t = super(SchemaSpot,cls).__new__(cls, name, bases, attrs)

        cls.schemas[schema_name] = t

        return t

class Schema(object):
    __metaclass__ = SchemaSpot

    def __init__(self, blog):
        self.blog = blog

    def get_query_set(self):
        raise NotImplementedError

    def get_data(self, params):
        count = params.get('count', 20)
        offset = params.get('offset', 0)
        field = params.get('field', None)
        direction = params.get("direction", None)

        query_set = self.get_query_set()

        res = []
        for line in query_set.values(*self.fields):
            res.append( dict([(name, smart_str(field)) for name, field in line.iteritems()]) )
        return {"source": res, "total": len(query_set)}

    def get_schema(self):
        pass
