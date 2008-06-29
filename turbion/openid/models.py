# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

from turbion.profiles.models import Profile

class IdentityManager( models.Manager ):
    def add_identifier( self, username, openid_url ):
        user = User.objects.get( username = username )

        identity, _ = self.get_or_create( user = user, url = openid_url )

        return identity

class Identity( models.Model ):
    user = models.ForeignKey( Profile, null = True, related_name = "openid_identifiers" )

    date = models.DateTimeField( default = datetime.now )

    last_login = models.DateTimeField( null = True, blank = True )
    url = models.URLField( max_length = 250, unique = True )

    objects = IdentityManager()

    class Meta:
        db_table = "turbion_openid_identity"
