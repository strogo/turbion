# -*- coding: utf-8 -*-

class ProcessorSpot(type):
    def __new__(cls, name, bases, attrs):
        try:
            BaseProcessor
        except NameError:
            cls.processors = {}

            return type.__new__(cls, name, bases, attrs)

        if not "name" in attrs:
            attrs["name"] = name.lower()

        t = type.__new__(cls, name, bases, attrs)

        descriptor = "%s.%s" % (t.__module__, name)
        t.descriptor = descriptor

        cls.processors[name] = t()

        return t

    @classmethod
    def get_processor(cls, name):
        for descriptor, proc in cls.processors.iteritems():
            if descriptor.endswith(name):
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
        return self.descriptor

    def __str__(self):
        return str(self.__unicode__())

    def __repr__(self):
        return self.__str__()
