# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class OnlyActiveBackend( ModelBackend ):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username, is_active = True)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None