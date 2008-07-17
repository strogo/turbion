# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.http import HttpRequest

from datetime import datetime

from turbion.visitors import managers
from turbion.profiles.models import Profile

from pantheon.models.models import ActionModel

class Visitor( models.Model, ActionModel ):
    session_key = models.CharField( max_length = 40 )

    name = models.CharField( max_length = 150, verbose_name = "имя", null = True, blank = True, )
    email = models.EmailField( null = True, blank = True, verbose_name = "e-mail" )
    site = models.CharField( max_length = 200, null = True, blank = True, verbose_name = "сайт" )
    #phone = models.CharField( maxlength = 200, null = True, blank = True, verbose_name = "телефон" )

    user = generic.GenericRelation("User", object_id_field="raw_user_id", content_type_field="raw_user_ct")

    objects = managers.VisitorManager()

    def __unicode__(self):
        return self.name and self.name or self.session_key

    def save(self):
        if self.site and not self.site.startswith( "http://" ):
            self.site = "http://" + self.site
        super( Visitor, self ).save()

    class Meta:
        verbose_name        = "visitor"
        verbose_name_plural = "visitors"
        db_table            = "turbion_visitor"

    class Admin:
        list_display = ( "name", "session_key", "email", "action_delete" )
        search_fields = ( "name", "email", "site" )
        list_per_page = 25

class CTChoices( object ):
    def __iter__(self):
        return iter( ( ( ContentType.objects.get( model = "profile",    app_label = "profiles" )    , "Зарегестрированный" ),
                 ( ContentType.objects.get( model = "visitor", app_label = "visitors" ), "Гость" ) ) )

class User( models.Model ):
    raw_user_ct = models.ForeignKey( ContentType,
                                     related_name = "users",
                                     verbose_name = "тип",
                                    # choices = CTChoices()
                                    )
    raw_user_id = models.PositiveIntegerField()

    raw_user = generic.GenericForeignKey( "raw_user_ct", "raw_user_id" )
    ip = models.IPAddressField( null = True )
    last_visit = models.DateTimeField( default = datetime.now )

    objects = managers.UserManager()

    guests     = managers.UserGenericManager( Visitor )
    registered = managers.UserGenericManager( Profile )

    @property
    def is_guest(self):
        return isinstance( self.raw_user, Visitor )

    def __unicode__(self):
        return "%s" % self.name

    @property
    def username(self):
        if self.is_guest:
            return self.raw_user.name
        else:
            return self.raw_user.username

    name = property( lambda self: self.raw_user.name )
    profile_name = name
    email = property( lambda self: self.raw_user.email )
    site = property( lambda self: self.raw_user.site )

    class Admin:
        list_display = ( "__unicode__", "email", "ip", "last_visit", "raw_user_ct" )
        list_per_page = 50
        list_filter = ( "ip", "raw_user_ct",  )

    class Meta:
        unique_together     = ( ( "raw_user_ct", "raw_user_id" ), )
        verbose_name        = "user"
        verbose_name_plural = "users"
        db_table            = "turbion_user"

def _get_visitor( self ):
    if not hasattr( self, "_visitor" ):
        try:
            self._visitor = Visitor.objects.get( session_key = self.session.session_key )
        except Visitor.DoesNotExist:
            self._visitor = None
    return self._visitor

def _get_generic_user( self ):
    if not getattr( self, "_generic_user", False ):
        if self.user.is_authenticated():
            raw_user = self.user.profile
        elif self.visitor:
            raw_user = self.visitor
        else:
            raw_user = None

        if raw_user:
            try:
                self._generic_user = User.objects.get_for( raw_user )
            except User.DoesNotExist:
                self._generic_user = None
        else:
            self._generic_user = None
    return self._generic_user

HttpRequest.visitor            = property( _get_visitor )
HttpRequest.generic_user       = property( _get_generic_user )
