# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from datetime import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from pantheon.postprocessing.fields import PostprocessField
from pantheon.utils.enum import Enum
from pantheon.models.manager import GenericManager

from turbion.profiles.models import Profile
from turbion.blogs.models import Blog

class Page( models.Model ):
    statuses = Enum( published = _( "published" ),
                     hide      = _( "hide" ) )
    blog        = models.ForeignKey( Blog, related_name = "pages" )

    created_on  = models.DateTimeField( default = datetime.now, verbose_name = _('creation date') )
    created_by  = models.ForeignKey( Profile, related_name = "created_pages" )

    edited_on   = models.DateTimeField( verbose_name = _('update date'), null = True, )
    edited_by   = models.ForeignKey( Profile, related_name = "edited_pages", null = True )

    slug        = models.SlugField()
    title       = models.CharField( max_length = 100, verbose_name = _( "title" ) )

    text        = models.TextField( verbose_name = _( "text" ) )
    text_html   = models.TextField( verbose_name = _( "text html" ) )

    status      = models.CharField( max_length = 10, choices = statuses, default = statuses.published )

    postprocess = PostprocessField()

    template    = models.CharField( max_length = 150, verbose_name = _( "template" ), null = True, blank = True )

    objects   = models.Manager()
    published = GenericManager( status = statuses.published )

    def __unicode__(self):
        return self.title

    def save( self ):
        if self.edited_by:
            self.edited_on = datetime.now()

        self.text_html = self.postprocess.postprocess( self.text )
        super( Feedback, self ).save()

    @models.permalink
    def get_absolute_url(self):
        return ( "pages_dispatcher", ( self.blog.slug, self.slug ) )

    class Admin:
        list_display = ( 'title', 'slug', 'created_by' )
        list_display_links = ( 'title', )

    class Meta:
        verbose_name        = _( "page" )
        verbose_name_plural = _( "pages" )
        db_table            = "turbion_page"
