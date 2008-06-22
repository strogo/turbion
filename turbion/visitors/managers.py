# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.db import models
from turbion.profiles.models import Profile

from django.contrib.contenttypes.models import ContentType

class VisitorManager( models.Manager ):
    def find( self, request ):
        try:
            visitor = self.get( session_key = request.session.session_key )
        except self.model.DoesNotExist:
            visitor = self.create( session_key = request.session.session_key )
        return visitor

class UserManager( models.Manager ):
    def _make_selectors( self, some_user ):
        from turbion.visitors.models import Visitor
        if not isinstance( some_user, ( Profile, Visitor ) ):
            raise ValueError, "User may be connected only to profile.Profile or visitors.Visitor objects"

        ct = ContentType.objects.get_for_model( some_user.__class__ )

        return { "raw_user_ct" : ct,
                 "raw_user_id" : some_user._get_pk_val()  }

    def create_user( self, some_user ):
        return self.create( **self._make_selectors( some_user ) )

    def get_for( self, some_user ):
        return self.get( **self._make_selectors( some_user ) )

    def get_or_create_for( self, some_user, defaults = {} ):
        lookups = self._make_selectors( some_user )
        try:
            user = self.get( **lookups )
            created = False
        except self.model.DoesNotExist:
            user = self.model( **lookups )
            user.__dict__.update( defaults )
            user.save()
            created = True
        return user, created

class UserGenericManager( models.Manager ):
    def __init__( self, user_model, **kwargs ):
        self.user_model = user_model
        self.lookups = kwargs

    @property
    def content_type(self):
        return ContentType.objects.get_for_model( self.user_model )

    def get_query_set(self):
        return super( UserGenericManager, self ).get_query_set().filter( raw_user_ct = self.content_type,
                                                                         **self.lookups )
