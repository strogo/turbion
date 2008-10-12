# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import signals

from turbion.options.option import BaseOption
from turbion.options.models import Option

class OptionSetCache( object ):
    def __init__( self ):
        self._sets = {}

    def add( self, name, set ):
        self._sets[ name ] = set

    def get_for_model( self, model ):
        res = []

        for set in self._sets.itervalues():
            if set._meta.model == model:
                res.append( set )
        return res

    def items( self ):
        return self._sets.items()

    def iteritems( self ):
        return self._sets.iteritems()

class OptionSetMeta( object ):
    def __init__( self, fields, descriptor, model = None, to_object = False ):
        self.fields = fields
        self.model = model
        self.to_object = to_object
        self.descriptor = descriptor

class OptionManager( object ):
    def __init__( self, option_set, object = None, cls = None ):
        setattr_method = self.__class__.__setattr__
        del self.__class__.__setattr__

        self.option_set = option_set
        self.object = object
        self.cls = cls
        self.__class__.__setattr__ = setattr_method

    def __getattr__( self, name ):
        return self.option_set.get( name, self.object, self.cls )

    def __setattr__( self, name, value ):
        self.option_set.set( name, value, self.object, self.cls )

class OptionSetDescriptor(object):
    def __init__(self, option_set):
        self.option_set = option_set

    def __get__(self, instance, instance_type=None):
        return OptionManager(self.option_set, cls=instance_type, object=instance)

    def __set__(self, instance, value):
        raise RuntimeError

def create_handler(option_set):
    def model_post_save_handler(sender, created, instance, **kwargs):
        if created:
            option_set.create(instance=instance)
    return model_post_save_handler

class OptionSetSpot(type):
    def __new__(cls, name, bases, attrs):
        try:
            OptionSet
        except NameError:
            cls.sets =  OptionSetCache()

            return super(OptionSetSpot, cls).__new__(cls, name, bases, attrs)

        if "Meta" in attrs:
            meta = attrs.pop("Meta")

            model = getattr(meta, "model", None)
            if not issubclass(model, ( models.Model,)):
                raise ValueError("model attribute must be django.db.models.Model class instance")

            to_object = getattr(meta, "to_object", False)
            set_name = getattr(meta, "name", "options")
        else:
            model = None
            to_object = False
            set_name = None

        fields = {}

        for key, field in attrs.items():
            if isinstance(field, BaseOption):
                attrs.pop(key)

                field.name = key
                fields[key] = field


        attrs[ "_meta" ] = OptionSetMeta( fields,
                                         None,
                                         model,
                                         to_object )

        t = super(OptionSetSpot, cls).__new__( cls, name, bases, attrs )

        instance = t()

        #TODO: add name checks
        if model:
            model.add_to_class(set_name, OptionSetDescriptor(instance))
        else:
            setattr(t, "instance", OptionSetDescriptor(instance))

        if model and to_object:
            signals.post_save.connect(create_handler(instance),
                                sender=model,
                                weak=False
                               )
            #TODO: add delete handler

        descriptor = "%s.%s" % (t.__module__, name)
        t._meta.descriptor = descriptor#FIXME: refactor descriptor assigment

        cls.sets.add(descriptor, instance)

        return t

class OptionSet(object):
    __metaclass__ = OptionSetSpot

    def get(self, name, object=None, cls=None):
        field = self._meta.fields.get(name, None)

        if not field:
            raise AttributeError("Option with name `%s` not found")

        try:
            return field.to_python(Option.active.get_option(name, self._meta.descriptor, object, cls).value)
        except Option.DoesNotExist:
            return None

    def set(self, name, value, object=None, cls=None):
        field = self._meta.fields.get(name, None)

        if not field:
            raise AttributeError("Option with name `%s` not found")

        Option.active.set_option(name, field.to_db(value), self._meta.descriptor, object, cls)

    def create(self, instance=None, pk=None):
        meta = self._meta
        if meta.to_object and meta.model:
            if pk is None and instance is None:
                raise ValueError

            if instance:
                pk = instance._get_pk_val()

            for name, option in meta.fields.iteritems():
                Option.active.add_option( option.name,
                                              option.to_db( option.default ),
                                              descriptor = meta.descriptor,
                                              cls = self._meta.model,
                                              id = pk )
        elif meta.model:
            for name, option in meta.fields.iteritems():
                Option.active.add_option(option.name,
                                        option.to_db( option.default ),
                                        descriptor = meta.descriptor,
                                        cls = meta.model )
        else:
            for name, option in meta.fields.iteritems():
                Option.active.add_option( option.name,
                                         option.to_db( option.default ),
                                         descriptor = meta.descriptor )
