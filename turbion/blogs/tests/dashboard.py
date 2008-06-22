# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
import re

from django.test import TestCase

from django.core.urlresolvers import reverse
from django.core import mail
from django import http
from django.conf import settings
from django.core import mail

from turbion.blogs.models import Blog, Post, Comment
from turbion.blogs.models.blog import BlogRoles
from turbion.blogs.utils import blog_reverse
from turbion.profiles.models import Profile

settings.DEBUG = True#FIXME: must accepts as `test` command param

CREDENTIALS = { 'username' : "daev", 'password' : "dkflbvbhgenby" }

class CreateBlogTest( TestCase ):
    fixtures = [ 'profiles' ]

    def setUp( self ):
        self.client.login( **CREDENTIALS )

    def test_index( self ):
        response = self.client.get( reverse( "dashboard_index" ) )
        self.assertRedirects( response, reverse( "dashboard_create_blog" ) )

    def test_create_blog( self ):
        response = self.client.get( reverse( "dashboard_create_blog" ) )

        self.assertEqual( response.status_code, http.HttpResponse.status_code )

        response = self.client.post( reverse( "dashboard_create_blog" ), data = { "name"  : "webnewage",
                                                                                  "slug"  : "wna",
                                                                                  "owner" : "1" } )

        self.assertEqual( response.status_code, http.HttpResponseRedirect.status_code )
        self.assertEqual( Blog.objects.count(), 1 )

class CreateSuperuser( TestCase ):
    def test_creation( self ):
        url = reverse( "dashboard_create_superuser" )
        response = self.client.get( url )

        self.assertEqual( response.status_code, http.HttpResponse.status_code )

        data = { "username"         : "daev",
                 "email"            : "foobar@dot.com",
                 "password"         : "foobar",
                 "password_confirm" : "foobar1"}

        response = self.client.post( url, data = data )

        self.assertEqual( response.status_code, http.HttpResponse.status_code )

        data[ "password_confirm" ] = "foobar"

        response = self.client.post( url, data = data )

        self.assertEqual( response.status_code, http.HttpResponseRedirect.status_code )
        self.assertEqual( Profile.objects.count(), 1 )


class DashboardTest( TestCase ):
    fixtures = [ 'blog', 'posts', 'profiles' ]

    def setUp( self ):
        self.user = Profile.objects.get( username = "daev" )
        self.blog = Blog.objects.get( slug = "wna" )

        BlogRoles.roles.blog_owner.grant( self.user, self.blog )

        self.client.login( **CREDENTIALS )

    def test_index_anon( self ):
        self.client.logout()
        response = self.client.get( self.blog.get_dashboard_url() )

        self.assertEqual( response.status_code, http.HttpResponseRedirect.status_code )

    def test_index( self ):
        response = self.client.get( self.blog.get_dashboard_url() )

        self.assertEqual( response.status_code, http.HttpResponse.status_code )

    def test_new_post( self ):
        response = self.client.get( reverse( "dashboard_blog_post_new", kwargs = { "blog" : "wna" } ) )
        self.assertEqual( response.status_code, http.HttpResponse.status_code )

    def test_edit_post( self ):
        pass
