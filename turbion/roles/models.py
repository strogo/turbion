# -*- coding: utf-8 -*-
from django.db import models

from turbion.utils.descriptor import DescriptorField, GenericForeignKey
from turbion.roles.managers import CapabilityManager, RoleManager

class Capability(models.Model):
    connection_dscr = DescriptorField(null=True)
    connection_id = models.PositiveIntegerField(null=True)

    connection = GenericForeignKey("connection_dscr", "connection_id")

    roleset = DescriptorField(max_length=250)#models.CharField(max_length=250)

    code = models.CharField(max_length=50, db_index=True)

    objects = CapabilityManager()

    def __unicode__(self):
        return self.code

    class Meta:
        unique_together = [("connection_id", "connection_dscr", "roleset", "code")]
        db_table        = "turbion_capability"

class Role(models.Model):
    code = models.CharField(max_length=150, db_index=True)
    roleset = DescriptorField(max_length=250)

    capabilities = models.ManyToManyField(Capability, related_name="roles")

    objects = RoleManager()

    def __unicode__(self):
        return self.code

    class Meta:
        db_table = "turbion_role"
