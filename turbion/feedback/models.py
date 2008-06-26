# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.db import models
from django.utils.translation import ugettext_lazy as _

from turbion.blogs.models import Blog
from turbion.notifications import EventDescriptor
from turbion.feedback import signals

from pantheon.models.models import ActionModel

class Feedback( ActionModel, models.Model ):
    blog = models.ForeignKey( Blog, related_name = "feedbacks" )
    name = models.CharField( max_length = 50, verbose_name = _('user') )
    e_mail = models.EmailField( verbose_name = _( 'e-mail' ) )
    date = models.DateTimeField( auto_now_add = True, verbose_name = _('creation date') )
    update_date = models.DateTimeField( auto_now = True, verbose_name = _('update date') )

    subject = models.CharField( max_length = 255, verbose_name = _( "subject" ) )

    text = models.TextField( verbose_name = _('text') )

    ip = models.IPAddressField()

    solved = models.BooleanField( default = False, verbose_name = _('checked') )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name        = _( 'feedback' )
        verbose_name_plural = _( 'feedbacks' )
        ordering            = ( 'solved', '-date', )
        db_table            = "turbion_feedback"

    class Admin:
        list_display = ( 'update_date', 'name', 'subject', 'e_mail', 'solved', 'ip', 'action_delete' )
        list_filter = ( "solved", "ip", "e_mail", )

class FeedbackAdd( EventDescriptor ):
    class Meta:
        name = _( "New feedback added" )

        trigger = ( Feedback, signals.feedback_added )
