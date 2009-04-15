import re

from django.test import TestCase

from django.core.urlresolvers import reverse
from django.core import mail
from django import http
from django.conf import settings
from django.core.management import call_command

from turbion.core.utils.testing import BaseViewTest

from turbion.core.blogs.models import Post, Comment, CommentAdd
from turbion.core.profiles.models import Profile

class SearchTest(BaseViewTest):
    fixtures = [
        'turbion/test/profiles',
        'turbion/test/blogs'
    ]

    def setUp(self):
        self.post = Post.objects.all()[0]

        CommentAdd.manager.subscribe(self.post.created_by, self.post)

        call_command("index", rebuild_index=True)

    def test_search(self):
        data = {
            "query": "test"
        }
        url = reverse("turbion_blog_search")
        self.assertStatus(url, data=data)

    def test_search_posts(self):
        pass

    def test_search_comments(self):
        pass
