# -*- coding: utf-8 -*-
import re

from django.test import TestCase

from django.core.urlresolvers import reverse
from django.core import mail
from django import http
from django.conf import settings
from django.core import mail

from turbion.utils.testing import BaseViewTest

from turbion.blogs.models import Blog, Post, Comment
from turbion.comments.models import CommentAdd
from turbion.blogs.models.blog import BlogRoles
from turbion.blogs.utils import blog_reverse
from turbion.profiles.models import Profile

CREDENTIALS = {'username': "daev", 'password': "foobar"}

class BlogViewsTest(BaseViewTest):
    fixtures = ['blog', 'posts', 'profiles', 'tags']

    def setUp(self):
        self.blog = Blog.objects.get(slug="wna")
        self.post = Post.objects.get(pk=1)
        
    def login(self):
        self.client.login(**CREDENTIALS)

    def test_index(self):
        self.assertStatus(self.blog.get_absolute_url())

    def test_post(self):
        self.login()
        self.assertStatus(self.post.get_absolute_url())

    def test_posts_feed(self):
        self.assertStatus(blog_reverse("blog_atom", args=(self.blog.slug, "posts")))

    def test_comments_feed(self):
        self.assertStatus(blog_reverse("blog_atom", args=(self.blog.slug, "comments")) )

    def test_post_comments_feed(self):
        self.assertStatus(blog_reverse("blog_atom", args=(self.blog.slug, "comments/%s/" % self.post.id)))

    def test_tag_feed(self):
        pass

    def test_sitemap(self):
        response = self.assertStatus(blog_reverse( "blog_sitemap", args=(self.blog.slug)))

    if settings.TURBION_BLOGS_MULTIPLE:
        def test_global_sitemap(self):
            response = self.assertStatus(blog_reverse("global_blog_sitemap"))

    def _create_comment(self):
        return {}

    def test_comment_add(self):
        url = blog_reverse("blog_comment_add", kwargs={"blog":self.blog.slug, "post_id":self.post.id})
        CommentAdd.instance.subscribe(self.post.created_by)

        self.login()

        comment = {"text": "My comment"}

        response = self.client.post(url, data=comment)

        self.assertEqual( response.status_code, http.HttpResponseRedirect.status_code )
        post = Post.published.for_blog( self.blog ).get( pk = self.post.pk )

        self.assertEqual(post.comment_count, 1)
        self.assertEqual(len( mail.outbox ), 1)# post author subscription

    def test_comment_add_visitor( self ):
        response = self.client.get( self.post.get_absolute_url() )

        HASH_RE = re.compile( "name=\"captcha_0\" value=\"(\w+)\"" )

        m = HASH_RE.search( response.content )
        if m:
            hash = m.groups()[0]

            test = manager.factory.get( hash )
            captcha = test.solutions[0]
        else:
            captcha = ""
            hash = ""

        url = blog_reverse("blog_comment_add", kwargs = {"blog": self.blog.slug, "post_id": self.post.id})

        comment = { "text"  : "My comment",
                    "name"  : "Alex",
                    "email" : "foo@bar.com",
                    "site"  : "http://foobar.com",
                    'notify': True,

                    "captcha_0" : hash,
                    "captcha_2" : captcha
                }

        response = self.client.post( url, data = comment )

        self.assertEqual( response.status_code, http.HttpResponseRedirect.status_code )
        post = Post.published.for_blog( self.blog ).get( pk = self.post.pk )

        self.assertEqual( post.comment_count, 1 )

        comment = Comment.objects.get()

        self.assertEqual( comment.created_by.name, "Alex" )
        self.assertEqual( len(CommentAdd._get_recipients(post)), 1 )

    def test_comment_edit( self ):
        pass

    def test_comment_delete( self ):
        self.test_comment_add()

        comment = Comment.objects.all()[0]
        response = self.assertStatus(reverse("comment_delete", args=(comment.id,)))

        post = Post.published.for_blog(self.blog).get(pk=self.post.pk)

        self.assertEqual(post.comment_count, 0)

    def test_archive_day(self):
        self.assertStatus(blog_reverse("blog_archive_year", args=(self.blog.slug, '2007', '12', '17')))

    def test_archive_month(self):
        self.assertStatus(blog_reverse("blog_archive_year", args=(self.blog.slug, '2006', '11')))

    def test_archive_year(self):
        self.assertStatus(blog_reverse("blog_archive_year", args=(self.blog.slug, '2007')))

    def test_tags(self):
        self.assertStatus(blog_reverse("blog_tags", args=(self.blog.slug,)))

    def test_tag(self):
        self.assertStatus(blog_reverse("blog_tag", args=(self.blog.slug, "foo")))
    
    if settings.TURBION_USE_DJAPIAN:
        def test_search(self):
            pass
    
        def test_search_posts(self):
            pass
    
        def test_search_comments(self):
            pass
