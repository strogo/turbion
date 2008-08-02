# -*- coding: utf-8 -*-
from django.db import models

class Site( models.Model ):
    name = models.CharField( max_length = 150 )
    url_pattern = models.CharField( max_length = 250 )
    image = models.ImageField( upload_to = "upload/socialbookmarks/", null = True, blank = True )

    def __unicode__(self):
        return self.name

    class Admin:
        pass

    class Meta:
        verbose_name        = "site"
        verbose_name_plural = "sites"
        db_table            = "turbion_socialbookmarks_site"

class Group( models.Model ):
    name = models.CharField( max_length = 150 )
    sites = models.ManyToManyField( Site )

    def __unicode__(self):
        return self.name

    class Admin:
        pass

    class Meta:
        verbose_name        = "group"
        verbose_name_plural = "groups"
        db_table            = "turbion_socialbookmarks_group"
