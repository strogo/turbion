# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
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
        verbose_name = "сайт"
        verbose_name_plural = "сайты"
    
class Group( models.Model ):
    name = models.CharField( max_length = 150 )
    sites = models.ManyToManyField( Site )
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        pass
    
    class Meta:
        verbose_name = "група"
        verbose_name_plural = "группы"