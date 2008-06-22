# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.db import models
from django.contrib.contenttypes.models import ContentType

class PermissionManager( models.Manager ):
    pass

class RoleManager( models.Manager ):
    pass
