# -*- coding: utf-8 -*-

class ProcessorSpot(type):
    def __new__(cls, name, bases, attrs):
        try:
            BaseProcessor
        except NameError:
            cls.processors = {}

            return type.__new__(cls, name, bases, attrs)

        if not "name" in attrs:
            processor_name = attrs["name"] = name.lower()
        else:
            processor_name = attrs["name"]

        t = type.__new__(cls, name, bases, attrs)
        t.descriptor = "%s.%s" % (t.__module__, name)

        cls.processors[processor_name] = t()

        return t

    @classmethod
    def get_processor(cls, name=None):
        name = str(name)#FIME: why convert to string. It must be string already!
        for proc_name, proc in cls.processors.iteritems():
            if proc_name.endswith(name):
                return proc
        raise ValueError("Postorocessor with name '%s' doesn't registered" % name)


class BaseProcessor(object):
    __metaclass__ = ProcessorSpot

    name = "BaseProcessor"

    def preprocess(self, value):
        raise NotImplementedError

    def postprocess(self, value):
        raise NotImplementedError

    def __unicode__(self):
        return self.name

    def __str__(self):
        return str(self.__unicode__())

    def __repr__(self):
        return self.__str__()
