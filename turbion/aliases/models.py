# -*- coding: utf-8 -*-
from django.db import models

from turbion.utils.models import GenericManager

class Alias(models.Model):
    from_url = models.CharField( max_length = 250, unique = True )
    to_url   = models.CharField( max_length = 250 )

    is_active = models.BooleanField( default = True )

    objects = models.Manager()
    active = GenericManager( is_active = True )

    class Meta:
        db_table = "turbion_alias"
