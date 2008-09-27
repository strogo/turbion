# -*- coding: utf-8 -*-
from django.utils.encoding import smart_str, smart_unicode

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

def get_attribute(obj, name):
    attr = getattr(obj, name)
    if callable(attr):
        attr = attr()
    return attr

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
        for obj in query_set:
            line = {}
            for field in self.fields:
                line[field] = smart_unicode(get_attribute(obj,field))
            res.append(line)

        return {"source": res, "total": len(query_set)}

    def get_schema(self):
        pass
