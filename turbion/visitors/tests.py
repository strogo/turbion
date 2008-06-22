# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.test import TestCase
from django.db import models
from django import newforms as forms

from turbion.profiles.models import Profile
from turbion.visitors.models import User, Visitor
from turbion.visitors.forms import combine_user_form_with

class Post( models.Model ):
    title = models.CharField( max_length = 20 )
    author = models.ForeignKey( User )

class PostModelForm( forms.ModelForm ):
    class Meta:
        model = Post
        exclude = ( "author", )

class PostForm( forms.Form ):
    title = forms.CharField()

class VisitorModelFormTest( TestCase ):
    """
    user = None
    """
    def setUp( self ):
        self.Form = combine_user_form_with( PostModelForm,
                                            user = None,
                                            visitor_data = { "session_key" : "foobar" },
                                            user_data = { "ip" : "0.0.0.0" },
                                            field = "author",
                                            need_captcha = False )
    def test_form_empty( self ):
        """
        post = None
        """
        form = self.Form()

        self.assert_( not form.is_valid() )

    def test_form_data( self ):
        """
        post = None
        """
        data = { "title" : "test title",
                 "name"  : "Alex" }

        form = self.Form( data = data )

        self.assert_( form.is_valid() )

        post = form.save()

        self.assert_( post._get_pk_val() is not None )
        self.assert_( post.author._get_pk_val() is not None )
        self.assert_( post.author.name, "Alex" )

    def _test_form_data_post( self ):
        """
        post = True
        """
        post = Post.objects.create( title = "Exist post" )

        data = { "title" : "test title",
                 "name"  : "Alex" }

        form = self.Form( data = data, instance = post )

        post = forms.save()

        self.assert_( post._get_pk_val() is not None )
        self.assertEqual( post.title, "test title" )
        self.assert_( post.author._get_pk_val() is not None )

class RegUserModelFormTest( TestCase ):
    def setUp( self ):
        """
        user = profile
        """
        raw_user = Profile.objects.create_user( "Alex", "foo@bar.com", "foobar" )
        self.user, _ = User.objects.get_or_create_for( raw_user, { "ip" : "0.0.0.0" } )

        self.Form = combine_user_form_with( PostModelForm,
                                            user = self.user,
                                            visitor_data = {},
                                            user_data = {},
                                            field = "author",
                                            need_captcha = False )

    def test_form_empty( self ):
        """
        post = None
        """
        form = self.Form()

        self.assert_( not form.is_valid() )

    def test_form_data( self ):
        """
        post = None
        """
        data = { "title" : "test title" }

        form = self.Form( data = data )

        self.assert_( form.is_valid() )

        post = form.save()

        self.assert_( post._get_pk_val() is not None )
        self.assertEqual( post.author._get_pk_val(), self.user._get_pk_val() )

#FIXME: repair test
class VisitorTestCase:#( TestCase ):
    def setUp(self):
        self.native_user = User.objects.create_user( "foo", "bar" )
        self.visitor = Visitor.objects.create( name="fuck" )

    def tearDown(self):
        pass

    def test_user_creation(self):
        generic_user1 = GenericUser.objects.create_user( self.native_user )
        self.assertEqual( generic_user1.type, GenericUser.GU_USER )
        self.assertEqual( generic_user1.name, "foo" )
        self.assertEqual( generic_user1.is_guest(), False )

    def test_visitor_creation(self):
        generic_user2 = GenericUser.objects.create_user( self.visitor )
        self.assertEqual( generic_user2.type, GenericUser.GU_VISITOR )
        self.assertEqual( generic_user2.name, "fuck" )
        self.assertEqual( generic_user2.is_guest(), True )

    def test_both_together(self):
        self.assertRaises( ValueError, GenericUser.objects.create, visitor = self.visitor, user = self.native_user )

    def test_no_one(self):
        self.assertRaises( ValueError, GenericUser.objects.create )
