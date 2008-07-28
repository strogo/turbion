# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.db import models


from pantheon.models.manager import GenericManager

class Alias( models.Model ):
    from_url = models.CharField( max_length = 250, unique = True )
    to_url   = models.CharField( max_length = 250 )

    is_active = models.BooleanField( default = True )

    objects = models.Manager()
    active = GenericManager( is_active = True )

    class Meta:
        db_table = "turbion_alias"
