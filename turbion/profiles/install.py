# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import dispatcher

def create_profile_for_user(sender, instance, *args, **kwargs):
    from turbion.profiles.models import Profile
    try:
        Profile.objects.get( user_ptr = instance )
    except Profile.DoesNotExist:
        p = Profile()
        p.__dict__.update( instance.__dict__ )
        p.save()

dispatcher.connect(create_profile_for_user, signal=signals.post_save, sender=User)
