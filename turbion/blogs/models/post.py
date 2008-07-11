# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007,2008 Alexander Koshelev (daevaorn@gmail.com)
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from turbion.notifications import EventDescriptor
from turbion.blogs import managers
from turbion.blogs.models.blog import Blog
from turbion.comments.models import Comment, CommentedModel
from turbion.tags.models import Tag
from turbion.tags.fields import TagsField
from turbion.profiles.models import Profile
from turbion.blogs import utils

from pantheon.models import fields
from pantheon.postprocessing.fields import PostprocessField
from pantheon.utils.enum import Enum

class Post( models.Model, CommentedModel ):
    statuses = Enum( draft     = _( "draft" ),
                     trash     = _( "trashed" ),
                     published = _( "published" )
                )

    commenting_settings = Enum( allow    = _( "allow" ),
                                disallow = _( "disallow" ),
            )

    show_settings = Enum( everybody = _( "everybody" ),
                          registred = _( "registered" ),
            )

    blog          = models.ForeignKey( Blog, verbose_name = _( "blog" ), related_name = "posts" )
    comment_count = models.PositiveIntegerField( default = 0, editable = False, verbose_name = _( "comment count" ) )

    created_on    = models.DateTimeField( default = datetime.now, editable = False, verbose_name = _( "created on" ) )
    created_by    = models.ForeignKey( Profile, related_name = "created_posts", verbose_name = _( "created by" ) )

    edited_on     = models.DateTimeField( null = True, editable = False, verbose_name = _( "edited on" ) )
    edited_by     = models.ForeignKey( Profile, null = True, blank = True, related_name = "edited_blogs", verbose_name = _( "edited by" ) )

    review_count  = models.IntegerField( default = 0, editable = False, verbose_name = _( "review count" ) )

    title         = models.CharField( max_length = 130, verbose_name = _( "title" ) )
    slug          = fields.ExtSlugField( for_field= "title", max_length = 130, editable = False, verbose_name = _( "slug" ) )

    mood          = models.CharField( max_length = 50, null = True, blank = True, verbose_name = _( "mood" ) )
    location      = models.CharField( max_length = 100, null = True, blank = True, verbose_name = _( "location" ) )
    music         = models.CharField( max_length = 100, null = True, blank = True, verbose_name = _( "music" ) )

    text          = models.TextField( verbose_name = _( "text" ) )
    text_html     = models.TextField( verbose_name = _( "text html" ) )

    status        = models.CharField( max_length = 10, choices = statuses, default = statuses.draft, verbose_name= _( "status" ) )

    postprocess   = PostprocessField( verbose_name = _( "postprocessor" ) )

    commenting    = models.CharField( max_length = 10,
                                      choices = commenting_settings,
                                      default = commenting_settings.allow,
                                      verbose_name = _( "commenting" ) )
    showing       = models.CharField( max_length = 10,
                                      choices = show_settings,
                                      default = show_settings.everybody,
                                      verbose_name= _( "showing" ) )

    notify        = models.BooleanField( default = True,
                                         verbose_name= _( "e-mail notifications" ) )

    draft   = property( lambda self: self.status == Post.statuses.draft )
    trash   = property( lambda self: self.status == Post.statuses.trash )
    publish = property( lambda self: self.status == Post.statuses.published )

    objects = managers.PostManager()

    published = managers.PostManager( status = statuses.published )
    trashed   = managers.PostManager( status = statuses.trash )
    drafts    = managers.PostManager( status = statuses.draft )

    tags = TagsField()

    @classmethod
    def get_for_pingback(cls, year_id, month_id, day_id, post_slug, **kwargs ):
        from django.shortcuts import get_object_or_404
        post = get_object_or_404( Post.published, created_on__year = year_id,
                                        created_on__month = month_id,
                                        created_on__day = day_id,
                                        slug = post_slug )
        return post

    @utils.permalink
    def get_absolute_url(self):
        return ( "turbion.blogs.views.post.post", (), { "year_id"   : self.created_on.year,
                                                         "month_id"  : self.created_on.month,
                                                         "day_id"    : self.created_on.day,
                                                         "post_slug" : self.slug,
                                                         "blog"      : self.blog.slug  } )

    def is_edited(self):
        return self.date < self.update_date

    @models.permalink
    def get_atom_feed_url(self):
        return ( "blog_atom", ( "%s/%s" % ( self.blog.slug, self.id ), ) )

    def inc_reviews(self):
        self.review_count += 1
        self.save()

    def per_page(self ):
        return self.get_preference().comments_per_page

    def __unicode__(self ):
        return self.title

    def save( self ):
        if self.edited_by:
            self.edited_on = datetime.now()

        self.text_html = self.postprocess.postprocess( self.text )
        super( Post, self ).save()

    class Admin:
        list_display       = ('blog', 'title', "created_by", 'created_on', 'status', 'comment_count', 'notify', 'review_count' )
        list_display_links = ( 'title', )
        list_filter        = ( 'blog', "created_by", "status", )
        list_per_page      = 50
        search_fields      = ( "title", "created_by__username" )

    class Meta:
        verbose_name        = 'post'
        verbose_name_plural = 'posts'
        ordering            = ( '-created_on', )
        unique_together     = ( ( "blog", "created_on", "title", "slug" ), )
        app_label           = "blogs"
        db_table            = "turbion_post"

from turbion.comments import signals as comment_signals

class CommentAdd( EventDescriptor ):
    class Meta:
        name = _( "new comment added" )

        trigger = ( Comment, comment_signals.comment_added )

    @classmethod
    def allow_recipient( cls, recipient, comment, *args, **kwargs ):
        if recipient == comment.created_by:
            return False
        return True
