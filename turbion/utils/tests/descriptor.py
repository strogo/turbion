# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models

from turbion.utils.descriptor import DescriptorField, GenericForeignKey, to_descriptor

class Host(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = "utils"

class Attribute(models.Model):
    descriptor = DescriptorField()
    object_id = models.PositiveIntegerField()

    connection = GenericForeignKey()

    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    class Meta:
        app_label = "utils"

class Descriptor(TestCase):
    def setUp(self):
        self.host = Host.objects.create(name="test")

        self.attr = Attribute.objects.create(
            descriptor=Host,
            object_id=self.host.id,
            name="test_attr",
            value="test"
        )

    def test_creation(self):
        self.assertEqual(self.attr.descriptor, Host)

    def test_fetch(self):
        attr = Attribute.objects.get()

        self.assertEqual(attr.descriptor, Host)

    def test_foreign_key(self):
        self.assertEqual(self.attr.connection, self.host)

    def test_foreign_key_set(self):
        new_host = Host.objects.create(name="new")

        self.attr.connection = new_host
        self.attr.save()

        attr = Attribute.objects.get()

        self.assertEqual(attr.connection, new_host)

    def test_descr_lookup(self):
        attrs = Attribute.objects.filter(descriptor=to_descriptor(Host))
        self.assertEqual(len(attrs), 1)
