# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals

def create_profile_for_user(sender, instance, created, *args, **kwargs):
    from turbion.profiles.models import Profile
    try:
        Profile.objects.get(user_ptr=instance)
    except Profile.DoesNotExist:
        p = Profile()
        p.__dict__.update(instance.__dict__)
        p.nickname = p.username
        p.save()

signals.post_save.connect(create_profile_for_user, sender=User)
