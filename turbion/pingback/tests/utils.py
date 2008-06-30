# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.dispatch import dispatcher
from django.db import models

from turbion.pingback import signals

class TestEntry( models.Model ):
    text = models.TextField()

    class Meta:
        app_label = "pingback"

    def get_absolute_url( self ):
        return "/entry/%s/" % self.id

    def process( self ):
        dispatcher.send( signal  = signals.send_pingback,
                        sender   = self.__class__,
                        instance = self,
                        url      = self.get_absolute_url(),
                        text     = self.text,
                )
