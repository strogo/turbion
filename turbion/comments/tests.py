# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.test import TestCase
from django.db import models

from turbion.comments.models import Comment
from turbion.comments import views
from turbion.visitors.models import User

class Article( models.Model ):
    title = models.CharField( max_length = 20 )

class CommentAddTest( TestCase ):
    def setUp( self ):
        self.article = Article.objects.create( title = "foobar" )

    def test_comment_add( self ):
        pass
