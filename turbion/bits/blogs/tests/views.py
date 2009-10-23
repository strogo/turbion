from django.test import TestCase

from django.core.urlresolvers import reverse
from django.core import mail
from django import http
from django.conf import settings
from django.core import mail

from turbion.bits.utils.testing import BaseViewTest

from turbion.bits.blogs.models import Post, Comment
from turbion.bits.profiles.models import Profile

class BlogsViews(BaseViewTest):
    fixtures = [
        'turbion/test/profiles',
        'turbion/test/blogs'
    ]

    def setUp(self):
        self.post = Post.objects.all()[0]

    def test_index(self):
        self.assertStatus(reverse("turbion_blog_index"))

    def test_post(self):
        self.assertStatus(self.post.get_absolute_url())

    def test_posts_feed(self):
        self.assertStatus(reverse("turbion_blog_atom", args=("posts",)))

    def test_comments_feed(self):
        self.assertStatus(reverse("turbion_blog_atom", args=("comments",)) )

    def test_post_comments_feed(self):
        self.assertStatus(
            reverse("turbion_blog_atom", args=("comments/%s/" % self.post.id,))
        )

    def test_tag_feed(self):
        pass

    def test_sitemap(self):
        response = self.assertStatus(reverse("turbion_sitemap", args=("posts",)))

    def test_index_sitemap(self):
        response = self.assertStatus(reverse("turbion_index_sitemap"))

    def _create_comment(self):
        return {}

    def test_comment_add(self):
        self.login()

        url = reverse("turbion_blog_comment_add", args=(self.post.id,))

        comment = {
            "text": "My comment",
            "text_filter": "markdown"
        }

        response = self.assertStatus(
            url,
            data=comment,
            status=http.HttpResponseRedirect.status_code,
            method="post"
        )

        post = Post.published.get(pk=self.post.pk)

        self.assertEqual(post.comment_count, 1)

    def test_comment_add_visitor(self):
        response = self.assertStatus(self.post.get_absolute_url())

        comment = self.hack_captcha(response)

        url = reverse("turbion_blog_comment_add", args=(self.post.id,))

        comment.update({
            "text": "My comment",
            "text_filter": "markdown",
            "nickname": "Alex",
        })

        response = self.assertStatus(
            url,
            data=comment,
            status=http.HttpResponseRedirect.status_code,
            method="post"
        )

        post = Post.published.get(pk=self.post.pk)

        self.assertEqual(post.comment_count, 1)

        comment = Comment.objects.get()

        self.assertEqual(comment.created_by.name, "Alex")

    def test_comment_delete(self):
        self.test_comment_add()

        comment = Comment.objects.all()[0]
        response = self.assertStatus(
            reverse("turbion_blog_comment_delete", args=(comment.pk,)),
            http.HttpResponseRedirect.status_code
        )

        post = Post.published.get(pk=self.post.pk)

        self.assertEqual(post.comment_count, 0)

    def test_archive_day(self):
        self.assertStatus(reverse("turbion_blog_archive_day", args=('2007', '12', '17')))

    def test_archive_month(self):
        self.assertStatus(reverse("turbion_blog_archive_month", args=('2006', '11')))

    def test_archive_year(self):
        self.assertStatus(reverse("turbion_blog_archive_year", args=('2007',)))

    def test_tag(self):
        self.assertStatus(reverse("turbion_blog_tag", args=("foo",)))

    def test_tags(self):
        self.assertStatus(reverse("turbion_blog_tags"))
