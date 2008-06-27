# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.db import models
from django.core.urlresolvers import reverse

from pantheon.postprocessing.fields import PostprocessField

from turbion.blogs.models import Blog

class Page( models.Model ):
    blog = models.ForeignKey( Blog, related_name = "pages" )

    slug = models.SlugField()
    title = models.CharField( max_length = 100, verbose_name = "Заголовок" )
    last_update = models.DateTimeField( auto_now = True, verbose_name = "Последнее обновление" )
    text = models.TextField( verbose_name = "Текст" )

    postprocess = PostprocessField()

    template = models.CharField( max_length = 150, verbose_name = "Шаблон", null = True, blank = True )

    def get_text(self):
        return self.postprocess.postprocess( self.text )

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse( "turbion.staticpages.views.dispatcher", kwargs = { 'slug' : self.slug } )

    class Admin:
        list_display = ( 'title', 'slug', 'last_update' )
        list_display_links = ( 'title', )

    class Meta:
        verbose_name        = "page"
        verbose_name_plural = "pages"
        db_table            = "turbion_page"
