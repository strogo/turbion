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

CREDENTIALS = {'username': "test", 'password': "test"}

class ViewsTest(BaseViewTest):
    fixtures = [
        'turbion/test/profiles',
        'turbion/test/blogs'
    ]

    def setUp(self):
        from turbion.comments.models import CommentAdd

        self.blog = Blog.objects.get(slug="test")
        self.post = Post.objects.filter(blog=self.blog)[0]

        CommentAdd.instance.subscribe(self.post.created_by, self.post)

    def login(self):
        self.client.login(**CREDENTIALS)

    def test_index(self):
        self.assertStatus(self.blog.get_absolute_url())

    def test_post(self):
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
        response = self.assertStatus(blog_reverse("blog_sitemap", args=(self.blog.slug,)))

    if settings.TURBION_BLOGS_MULTIPLE:
        def test_global_sitemap(self):
            response = self.assertStatus(blog_reverse("global_blog_sitemap"))

    def _create_comment(self):
        return {}

    def test_comment_add(self):
        self.login()

        url = blog_reverse("blog_comment_add", kwargs={"blog": self.blog.slug, "post_id": self.post.id})
        CommentAdd.instance.subscribe(self.post.created_by)

        comment = {"text": "My comment"}

        response = self.assertStatus(
                        url,
                        data=comment,
                        status=http.HttpResponseRedirect.status_code,
                        method="post"
                )

        post = Post.published.for_blog(self.blog).get(pk=self.post.pk)

        self.assertEqual(post.comment_count, 1)
        self.assertEqual(len(mail.outbox), 1)# post author subscription
        self.assertEqual(len(CommentAdd()._get_recipients(post)), 1)

    def test_comment_add_visitor(self):
        response = self.assertStatus(self.post.get_absolute_url())

        comment = self.hack_captcha(response)

        url = blog_reverse("blog_comment_add", args=(self.blog.slug, self.post.id))

        comment.update({
                    "text"    : "My comment",
                    "nickname": "Alex",
                    "email"   : "foo@bar.com",
                    "site"    : "http://foobar.com",
                    'notify'  : True,
        })

        response = self.assertStatus(
                        url,
                        data=comment,
                        status=http.HttpResponseRedirect.status_code,
                        method="post"
                )

        post = Post.published.for_blog(self.blog).get(pk=self.post._get_pk_val())

        self.assertEqual(post.comment_count, 1)

        comment = Comment.objects.get()

        self.assertEqual(comment.created_by.name, "Alex")
        self.assertEqual(len(CommentAdd()._get_recipients(post)), 2)

    def test_comment_delete(self):
        self.test_comment_add()

        comment = Comment.objects.all()[0]
        response = self.assertStatus(
                    reverse("comment_delete", args=(comment._get_pk_val(),)),
                    http.HttpResponseRedirect.status_code
                )

        post = Post.published.for_blog(self.blog).get(pk=self.post.pk)

        self.assertEqual(post.comment_count, 0)

    def test_archive_day(self):
        self.assertStatus(blog_reverse("blog_archive_day", args=(self.blog.slug, '2007', '12', '17')))

    def test_archive_month(self):
        self.assertStatus(blog_reverse("blog_archive_month", args=(self.blog.slug, '2006', '11')))

    def test_archive_year(self):
        self.assertStatus(blog_reverse("blog_archive_year", args=(self.blog.slug, '2007')))

    def test_tag(self):
        self.assertStatus(blog_reverse("blog_tag", args=(self.blog.slug, "foo")))

    def test_tags(self):
        self.assertStatus(blog_reverse("blog_tags", args=(self.blog.slug,)))

    if settings.TURBION_USE_DJAPIAN:
        def test_search(self):
            pass

        def test_search_posts(self):
            pass

        def test_search_comments(self):
            pass
