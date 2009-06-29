from django.utils import simplejson

mime_types = ['application/json']

def generator(openids, buf):
    simplejson.dump(list(openids), buf)

def parser(content):
    return simplejson.loads(content)
