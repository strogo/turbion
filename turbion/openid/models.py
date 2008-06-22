# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

from turbion.profiles.models import Profile

class Identifier( models.Model ):
    user = models.ForeignKey( Profile, null = True, related_name = "openid_identifiers" )

    date = models.DateTimeField( default = datetime.now )

    last_login = models.DateTimeField( null = True, blank = True )
    url = models.UrlField( max_length = 250, unique = True )
