# -*- coding: utf-8 -*-
from django.db import models

def to_descriptor(model):
    meta = model._meta
    return "%s.%s" % (meta.app_label, meta.object_name.lower())

def to_model(dscr):
    app_name, model = dscr.split(".", 1)

    return models.get_model(app_name, model)

class DescriptorField(models.CharField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, max_length=100, *args, **kwargs):
        super(DescriptorField, self).__init__(max_length=max_length, *args, **kwargs)

    def _check_descriptable(self, value):
        return isinstance(value, type)\
                and issubclass(value, models.Model)\
                and value is not None

    def to_python(self, value):
        if self._check_descriptable(value):
            return value

        if value is not None:
            return to_model(value)

    def get_db_prep_value(self, value):
        if self._check_descriptable(value):
            return to_descriptor(value)

        return value

class GenericForeignKey(object):
    def __init__(self, dscr_field="descriptor", pk_field="object_id"):
        self.dscr_field = dscr_field
        self.pk_field = pk_field

    def contribute_to_class(self, cls, name):
        self.name = name
        self.model = cls
        self.cache_attr = "_%s_cache" % name

        setattr(cls, name, self)

    def __get__(self, instance, instance_type=None):
        if instance is None:
            raise AttributeError, u"%s must be accessed via instance" % self.name

        try:
            return getattr(instance, self.cache_attr)
        except AttributeError:
            rel_obj = None

            f = self.model._meta.get_field(self.dscr_field)
            descriptor = getattr(instance, f.get_attname(), None)
            if descriptor:
                try:
                    rel_obj = descriptor._default_manager.get(pk=getattr(instance, self.pk_field))
                except models.ObjectDoesNotExist:
                    pass

            setattr(instance, self.cache_attr, rel_obj)
            return rel_obj

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError, u"%s must be accessed via instance" % self.related.opts.object_name

        descriptor = None
        pk = None
        if value is not None:
            descriptor = value.__class__
            pk = value._get_pk_val()

        setattr(instance, self.dscr_field, descriptor)
        setattr(instance, self.pk_field, pk)
        setattr(instance, self.cache_attr, value)
