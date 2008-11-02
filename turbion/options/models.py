# -*- coding: utf-8 -*-
from django.db import models

from turbion.utils.descriptor import DescriptorField, GenericForeignKey
from turbion.utils.models import GenericManager

class OptionManager(GenericManager):
    def _make_lookup(self, object, cls, id=None):
        from turbion.utils.descriptor import to_descriptor

        if cls and not issubclass(cls, (models.Model,)):
            cls = None
        return {
            "connection_dscr": cls and to_descriptor(cls) or None,
            "connection_id": id and id or (object and object._get_pk_val() or None)
        }

    def add_option(self, name, value, descriptor, object=None, cls=None, id=None):
        connection_lookup = self._make_lookup(object, cls, id)
        try:
            option = self.get(name=name, descriptor=descriptor, **connection_lookup)
            option.value = value
            option.save()
        except self.model.DoesNotExist:
            option = self.create(name=name,
                                value=value,
                                descriptor=descriptor,
                                **connection_lookup
                              )
        return option

    def has_option(self, name, object=None, cls=None):
        try:
            self.get_option(name, object, cls)
            return True
        except self.model.DoesNotExist:
            return False

    def get_option(self, name, descriptor, object=None, cls=None):
        connection_lookup = self._make_lookup(object, cls)
        return self.get(name=name, descriptor=descriptor, **connection_lookup)

    def set_option(self, name, value, descriptor, object=None, cls=None):
        option = self.get_option(name, descriptor, object, cls)
        option.value = value
        option.save()

class Option(models.Model):
    connection_dscr = DescriptorField(null=True)
    connection_id = models.PositiveIntegerField(null=True)

    connection = GenericForeignKey("connection_dscr", "connection_id")

    descriptor = DescriptorField()
    name = models.CharField(max_length=100, db_index=True)
    value = models.TextField(null=True)

    is_active = models.BooleanField(default=True)

    objects = OptionManager()
    active = OptionManager(is_active=True)

    class Meta:
        unique_together = [("connection_id", "connection_dscr", "descriptor", "name")]
        db_table        = "turbion_option"
