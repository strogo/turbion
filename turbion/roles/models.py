# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.dispatch import dispatcher

from turbion.roles.managers import PermissionManager, RoleManager

class Capability( models.Model ):
    connection_ct = models.ForeignKey( ContentType, related_name = "capabilities", null = True )
    connection_id = models.PositiveIntegerField( null = True )

    connection = GenericForeignKey( "connection_ct", "connection_id" )

    descriptor = models.CharField( max_length = 250 )

    code = models.CharField( max_length = 50, db_index = True )

    objects = PermissionManager()

    def __unicode__( self ):
        return self.code

    class Meta:
        unique_together = [ ( "connection_id", "connection_ct", "descriptor", "code" ) ]

class Role( models.Model ):
    code = models.CharField( max_length = 150, db_index = True )
    descriptor = models.CharField( max_length = 250 )

    capabilities = models.ManyToManyField( Capability, related_name = "roles" )

    objects = RoleManager()

    def get_roleset( self ):
        mod, name = self.descriptor.rsplit( '.', 1 )
        return getattr( __import__( mod, {}, {}, [ "" ] ), name )

    def __unicode__( self ):
        return self.code

    class Meta:
        pass
