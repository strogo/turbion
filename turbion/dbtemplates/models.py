# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007-2008 Alexander Koshelev (daevaorn@gmail.com)
from django.db import models

from pantheon.models import manager
from pantheon.models.models import ActionModel

class Template( ActionModel, models.Model ):
    path = models.CharField( max_length = 250, unique = True )
    is_active = models.BooleanField( default = True )
    text = models.TextField()

    objects = models.Manager()
    active = manager.GenericManager( is_active = True )

    def __unicode__(self):
        return self.path

    class Admin:
        list_display = ( "path", "is_active", "action_delete" )
        list_filter = ( "is_active", )

    class Meta:
        verbose_name = "шаблон"
        verbose_name_plural = "шаблоны"