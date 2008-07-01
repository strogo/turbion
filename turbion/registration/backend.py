# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.contrib.auth.backends import ModelBackend
from turbion.profiles.models import Profile

class OnlyActiveBackend( ModelBackend ):
    def authenticate(self, username=None, password=None):
        try:
            user = Profile.objects.get(username=username, is_active = True)
            if user.check_password(password):
                return user
        except Profile.DoesNotExist:
            return None