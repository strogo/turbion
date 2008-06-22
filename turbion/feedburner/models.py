# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007-2008 Alexander Koshelev (daevaorn@gmail.com)
import feedburner

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from pantheon.models.models import ActionModel

class Account( models.Model ):
    user = models.ForeignKey( User, unique = True )

    name = models.CharField( max_length = 100 )
    password = models.CharField( max_length = 100 )

    base_name = models.CharField( max_length = 150, unique = True )

    def get_management(self):
        return feedburner.Management( self.name, self.password )

    def __unicode__(self):
        return "%s: %s" % ( self.user, self.name )

    class Admin:
        pass

    class Meta:
        verbose_name = "аккаунт"
        verbose_name_plural = "аккаунты"

class Feed( ActionModel, models.Model ):
    account = models.ForeignKey( Account )

    name = models.CharField( max_length = 150 )
    source = models.CharField( max_length = 255 )

    created = models.BooleanField( default = False )

    def __unicode__(self):
        return "%s: %s" % ( self.name, self.source )

    def get_feedburner_url(self):
        return "http://feeds.feedburner.com/%s" % self.name

    def get_feed(self):
        return self.account.get_management().get( uri = self.name )

    def add(self):
        manager = self.account.get_management()
        return manager.add( feedburner.Feed( source = "http://%s%s" % ( Site.objects.get_current().domain, self.source ),
                                      uri = self.name,
                                      title = self.name ) )

    def create(self):
        from django.core.urlresolvers import reverse
        if not self.created:
            return '<a href="%s">Create</a>' % reverse( "turbion.feedburner.views.add_to_feedburner", args = (self.id,) )
        return ""
    create.allow_tags = True

    class Admin:
        list_display = ( "source", "name", "account", "created", "get_feedburner_url", "create", "action_delete" )
        list_filter = ( "created", "account" )
        list_per_page = 25

    class Meta:
        verbose_name = "фид"
        verbose_name_plural = "фиды"