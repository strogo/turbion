# -*- coding: utf-8 -*-
from django.db import models
from django.test import TestCase
from django import forms

from turbion.tags.models import Tag
from turbion.tags.fields import TagsField
from turbion.tags import forms as tags_forms

class Article( models.Model ):
    title = models.CharField( max_length = 50 )

    tags = TagsField()

class ArticleForm( forms.ModelForm ):
    class Meta:
        model = Article

    def __init__( self, *args, **kwargs ):
        super( ArticleForm, self ).__init__( *args, **kwargs )

        self.fields[ "tags" ] = tags_forms.TagsField( form = self )

class TagsTest( TestCase ):
    tags = [ "foo", "bar", "foo bar" ]

    def setUp( self ):
        self.article = Article.objects.create( title = "great header" )

    def test_add_tags_str( self ):
        self.article.tags.add( *self.tags )

        self.assertEqual( set( self.tags ),
                          set( Tag.objects.all().values_list( "name", flat = True ) ) )

    def test_add_tags_mixed( self ):
        tag1 = Tag.objects.create( name = self.tags[ 0 ] )
        tag2 = Tag.objects.create( name = self.tags[ 1 ] )

        self.article.tags.add( tag1.id, tag2, self.tags[ 2 ] )

        self.assertEqual( set( [ t.name for t in self.article.tags.all() ] ),
                          set( self.tags )
                        )

    def test_get_tags( self ):
        self.article.tags.add( *self.tags )

        Article.objects.create( title = "fake" ).tags.add( "fake tag", "fake tag 2" )

        self.assertEqual( set( [ t.name for t in self.article.tags.all() ] ),
                          set( self.tags )
                        )

    def test_remove_tags( self ):
        self.article.tags.add( *self.tags )

        self.article.tags.remove( "foo" )

        self.assertEqual( set( self.article.tags.all_name()),
                          set( self.tags[1:] )
                        )

    def test_add_form( self ):
        self.article.tags.add( *self.tags )#adding tags to model

        data = { "title"  : "foobar",
                 "tags_0" : [ 1, 2 ],
                 "tags_1" : "barfoo" }

        form = ArticleForm( data = data )

        self.assert_( form.is_valid() )

        article = form.save()
        form.save_tags()

        self.assertEqual( set( article.tags.all_name()),
                          set( self.tags[:-1] + [ "barfoo" ] ) )

    def test_edit_form( self ):
        self.article.tags.add( *self.tags )

        data = { "title"  : "foobar",
                 "tags_0" : [ 1, 2 ],
                 "tags_1" : "barfoo" }

        form = ArticleForm( instance = self.article,
                            data = data )

        self.assert_( form.is_valid() )

        article = form.save()
        form.save_tags()

        self.assertEqual( set( article.tags.all_name()),
                          set( self.tags[:-1] + [ "barfoo" ] ) )
