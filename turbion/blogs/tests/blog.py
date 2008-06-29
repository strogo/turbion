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

from turbion.blogs.models import Blog, Post, Comment, CommentAdd
from turbion.blogs.models.blog import BlogRoles
from turbion.blogs.utils import blog_reverse
from turbion.profiles.models import Profile

settings.DEBUG = True#FIXME: must accepts as `test` command param

CREDENTIALS = { 'username' : "daev", 'password' : "dkflbvbhgenby" }

class BlogTest( TestCase ):
    fixtures = [ 'blog', 'posts', 'profiles', 'tags' ]

    def assertOk( self, url ):
        response = self.client.get( url )

        self.assertEqual( response.status_code, http.HttpResponse.status_code )

        return response

    def setUp( self ):
        self.blog = Blog.objects.get( slug = "wna" )
        self.post = Post.objects.get( pk = 1 )

    def test_index( self ):
        response = self.client.get( self.blog.get_absolute_url() )

        self.assertEqual( response.status_code, http.HttpResponse.status_code )

    def test_post( self ):
        self.client.login( **CREDENTIALS )

        response = self.client.get( self.post.get_absolute_url() )

        self.assertEqual( response.status_code, http.HttpResponse.status_code )

    def test_posts_feed( self ):
        url = blog_reverse( "blog_atom", kwargs = { 'blog' : self.blog.slug,
                                                    'url' : "posts" } )
        self.assertOk( url )

    def test_comments_feed( self ):
        url = blog_reverse( "blog_atom", kwargs = { 'blog' : self.blog.slug,
                                                    'url'  : "comments" } )
        self.assertOk( url )

    def test_post_comments_feed( self ):
        url = blog_reverse( "blog_atom", kwargs = { 'blog' : self.blog.slug,
                                                    'url'  : "comments/%s/" % self.post.id } )
        self.assertOk( url )

    def test_tag_feed( self ):
        pass

    def test_sitemap( self ):
        url = blog_reverse( "blog_sitemap", kwargs = { 'blog' : self.blog.slug } )

        response = self.assertOk( url )
        #TODO: check right data

    if settings.TURBION_BLOGS_MULTIPLE:
        def test_global_sitemap( self ):
            url = blog_reverse( "global_blog_sitemap" )

            response = self.assertOk( url )
            #TODO: check right data

    def _create_comment( self ):
        return {}

    def test_comment_add( self ):
        url = blog_reverse( "blog_comment_add", kwargs = { "blog" : self.blog.slug, "post_id" : self.post.id } )
        CommentAdd.subscribe( self.post.created_by )

        self.client.login( **CREDENTIALS )

        comment = { "text" : "My comment" }

        response = self.client.post( url, data = comment )
        self.assertEqual( response.status_code, http.HttpResponseRedirect.status_code )
        post = Post.published.for_blog( self.blog ).get( pk = self.post.pk )

        self.assertEqual( post.comment_count, 1 )
        self.assertEqual( len( mail.outbox ), 1 )# post author subscription

    def test_comment_add_visitor( self ):
        response = self.client.get( self.post.get_absolute_url() )

        HASH_RE = re.compile( "name=\"captcha_0\" value=\"(\w+)\"" )

        m = HASH_RE.search( response.content )
        if m:
            hash = m.groups()[0]
            from pantheon.supernovaforms.captcha import manager

            test = manager.factory.get( hash )
            captcha = test.solutions[0]
        else:
            captcha = ""
            hash = ""

        url = blog_reverse( "blog_comment_add", kwargs = { "blog" : self.blog.slug, "post_id" : self.post.id } )

        comment = { "text"  : "My comment",
                    "name"  : "Alex",
                    "email" : "foo@bar.com",
                    "site"  : "http://foobar.com",

                    "captcha_0" : hash,
                    "captcha_2" : captcha
                }

        response = self.client.post( url, data = comment )

        self.assertEqual( response.status_code, http.HttpResponseRedirect.status_code )
        post = Post.published.for_blog( self.blog ).get( pk = self.post.pk )

        self.assertEqual( post.comment_count, 1 )

        comment = Comment.objects.get()

        self.assertEqual( comment.created_by.name, "Alex" )

    def test_comment_edit( self ):
        pass

    def test_comment_delete( self ):
        self.test_comment_add()

        comment = Comment.objects.all()[0]

        response = self.client.get( reverse( "comment_delete", args = ( comment.id, ) ) )

        self.assertEqual( response.status_code, http.HttpResponseRedirect.status_code )

        post = Post.published.for_blog( self.blog ).get( pk = self.post.pk )

        self.assertEqual( post.comment_count, 0 )

    def test_archive_day( self ):
        response = self.client.get( blog_reverse( "blog_archive_year", args = ( self.blog.slug, '2007', '12', '17' ) ) )

        self.assertEqual( response.status_code, http.HttpResponse.status_code )

    def test_archive_month( self ):
        response = self.client.get( blog_reverse( "blog_archive_year", args = ( self.blog.slug, '2006', '11' ) ) )

        self.assertEqual( response.status_code, http.HttpResponse.status_code )

    def test_archive_year( self ):
        response = self.client.get( blog_reverse( "blog_archive_year", args = ( self.blog.slug, '2007') ) )

        self.assertEqual( response.status_code, http.HttpResponse.status_code )

    def test_tags( self ):
        response = self.client.get( blog_reverse( "blog_tags", args = ( self.blog.slug, ) ) )

        self.assertEqual( response.status_code, http.HttpResponse.status_code )

    def test_tag( self ):
        response = self.client.get( blog_reverse( "blog_tag", args = ( self.blog.slug, "foo" ) ) )

        self.assertEqual( response.status_code, http.HttpResponse.status_code )

    def test_search( self ):
        pass

    def test_search_posts( self ):
        pass

    def test_search_comments( self ):
        pass
