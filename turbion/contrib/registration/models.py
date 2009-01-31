# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime

from turbion.utils.enum import Enum

from turbion.profiles.models import Profile

class Offer(models.Model):
    code_types = Enum(registration    ="registration",
                      email_change    ="email_change",
                      password_restore="password_restore"
            )

    user = models.ForeignKey(Profile)
    type = models.CharField(max_length=50, default=code_types.registration, choices=code_types)
    date = models.DateTimeField(default=datetime.now)#TODO:cleanup old codes
    code = models.CharField(max_length=128, unique=True)
    data = models.CharField(max_length=250, null=True, blank=True)

    def gen_code(self):
        import md5
        import random
        return md5.new(
                    self.user.username\
                    + self.user.email\
                    + str(random.random())
                ).hexdigest()

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.gen_code()
        super(Offer, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username

    class Meta:
        unique_together     = [("type", "user")]
        verbose_name        = "reg code"
        verbose_name_plural = "reg codes"
        db_table            = "turbion_reg_offer"
