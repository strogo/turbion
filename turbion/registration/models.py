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

from pantheon.utils.enum import Enum

class IllegalName( models.Model ):
    name = models.CharField( max_length = 50 )

    def __unicode__(self):
        return self.name

    class Admin:
        pass

    class Meta:
        verbose_name = "запретное имя"
        verbose_name_plural = "запретные имена"

class Code( models.Model ):
    code_types = Enum( registration = "registration",
                   email_change = "email_change",
                   password_restore = "password_restore"
              )

    user = models.ForeignKey( User )
    type = models.CharField( max_length = 50, default=code_types.registration, choices = code_types )
    date = models.DateTimeField( default = datetime.now )#TODO:cleanup old codes
    code = models.CharField( max_length = 128, unique = True )
    data = models.CharField( max_length = 250, null = True, blank = True )

    def gen_code(self):
        import md5
        return md5.new(self.user.username + self.user.email ).hexdigest()

    def save(self):
        if not self.code:
            self.code = self.gen_code()
        super( Code, self ).save()

    def __unicode__(self):
        return self.user.username

    class Admin:
        list_display = ( "user", "type", "date", "code", "data" )

    class Meta:
        unique_together = ( ( "type", "user"), )
        verbose_name = "запрос"
        verbose_name_plural = "запросы"
