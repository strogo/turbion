# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.db import models, connection
from django.conf import settings
from django.dispatch import dispatcher
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from datetime import datetime

from turbion.visitors.models import User
from turbion.profiles.models import Profile

from pantheon.postprocessing.fields import PostprocessField
from pantheon.models.models import ActionModel
from pantheon.models import manager
from pantheon.utils.enum import Enum

quote_name = connection.ops.quote_name

class CommentedModel( object ):
    def update_comment_count( self ):
        self.comment_count = Comment.published.for_object( self ).count()
        self.save()

class CommentManager( manager.GenericManager ):
    def for_model_with_rel( self, model, obj ):
        ct = ContentType.objects.get_for_model( model )

        for field in  model._meta.fields:
            if isinstance( field, models.ForeignKey ):
                if field.rel.to == obj.__class__:
                    return self.filter( connection_ct = ct ).extra( where = [ "%s.%s= %s" % ( quote_name( model._meta.db_table ), quote_name( field.column ), getattr( obj, field.rel.field_name ) ) ],
                                                                    tables = [ model._meta.db_table ] )

        raise ValueError, "Model %s has no relations to %s" % ( model, obj.__class__ )

    def for_object( self, obj ):
        ct = ContentType.objects.get_for_model( obj.__class__ )

        return self.filter( connection_ct = ct,
                            connection_id = obj._get_pk_val() )

class Comment( ActionModel, models.Model ):
    connection_ct = models.ForeignKey( ContentType, editable = False )
    connection_id = models.PositiveIntegerField( editable = False )
    connection = generic.GenericForeignKey( "connection_ct", "connection_id" )

    statuses = Enum( published  = "published",
                     moderation = "on moderation", )

    created_on = models.DateTimeField( default = datetime.now, verbose_name = _( "created on" ) )
    created_by = models.ForeignKey( User, related_name = "created_comments", verbose_name = _( "created by" ), raw_id_admin = True )

    edited_on = models.DateTimeField( null = True, verbose_name = _( "edited on" ) )
    edited_by = models.ForeignKey( Profile, related_name = "edited_comments", null = True, verbose_name = _( "edited by" ) )

    text = models.TextField( verbose_name = _( "text" ) )
    text_html   = models.TextField( verbose_name = _( "text html" ) )

    status = models.CharField( max_length = 20,
                               choices = statuses,
                               default = statuses.published,
                               verbose_name = _( "status" ) )

    notify = models.BooleanField( default= False, verbose_name = _( "e-mail notifications" ) )

    postprocess = PostprocessField( verbose_name = _( "postprocessor" ) )

    is_published = property( lambda self: self.status == Comment.statuses.published )

    objects = CommentManager()
    published = CommentManager( status = statuses.published )

    def is_edited(self):
        return self.created_on != self.edited_on

    def __unicode__(self):
        return "%s - %s" % (self.created_by.name, self.created_on)

    def get_absolute_url( self ):
        return self.connection.get_absolute_url() +"#comment_%s" % self.id

    def save( self ):
        if self.edited_by:
            self.edited_on = datetime.now()

        self.text_html = self.postprocess.postprocess( self.text )

        super( Comment, self ).save()

    class Meta:
        ordering            = ( "created_on",)
        verbose_name        = _( 'comment' )
        verbose_name_plural = _( 'comments' )
        db_table            = "turbion_comment"


def update_comment_count(connection):
    try:
        connection.update_comment_count()
    except AttributeError:
        pass

def post_save(instance, created):
    if created:
        update_comment_count(instance.connection)

def post_delete( instance ):
    update_comment_count(instance.connection)

dispatcher.connect(post_save,   sender = Comment, signal = signals.post_save)
dispatcher.connect(post_delete, sender = Comment, signal = signals.post_delete)
