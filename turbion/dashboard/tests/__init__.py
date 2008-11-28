# -*- coding: utf-8 -*-
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
from turbion.utils.testing import BaseViewTest

class CreateBlogTest(BaseViewTest):
    fixtures = ['turbion/test/profiles']

    def setUp(self):
        self.login()

    def test_index(self):
        response = self.client.get(reverse("turbion_dashboard_index"))
        self.assertRedirects(response, reverse("turbion_dashboard_create_blog"))

    def test_create_blog(self):
        response = self.client.get(reverse("turbion_dashboard_create_blog"))

        self.assertResponseStatus(response, http.HttpResponse.status_code)

        data={
            "name": "webnewage",
            "slug": "wna",
            "owner": "1"
        }

        response = self.client.post(reverse("turbion_dashboard_create_blog"), data=data)

        self.assertEqual(response.status_code, http.HttpResponseRedirect.status_code)
        self.assertEqual(Blog.objects.count(), 1)

class CreateSuperuser(BaseViewTest):
    def test_creation(self):
        url = reverse("turbion_dashboard_create_superuser")
        self.assertStatus(
                url,
                http.HttpResponse.status_code
        )

        data = {
            "username": "daev",
            "email": "foobar@dot.com",
            "new_password1": "foobar",
            "new_password2": "foobar1"
        }

        self.assertStatus(url, http.HttpResponse.status_code, data=data)

        data["new_password2"] = "foobar"

        response = self.client.post(url, data=data)

        self.assertStatus(url, http.HttpResponseRedirect.status_code, data=data)
        self.assertEqual(Profile.objects.count(), 1)


class DashboardTest(BaseViewTest):
    fixtures = [
        'turbion/test/blogs', 'turbion/test/posts', 'turbion/test/profiles'
    ]

    def setUp(self):
        self.blog = Blog.objects.all()[0]

        BlogRoles.roles.blog_owner.grant(self.user, self.blog)

        self.login()

    def test_index_anon(self):
        self.client.logout()

        self.assertStatus(
            self.blog.get_dashboard_url(),
            http.HttpResponseRedirect.status_code
        )

    def test_index(self):
        self.assertStatus(
            self.blog.get_dashboard_url(),
            http.HttpResponse.status_code
        )

    def test_new_post(self):
        self.assertStatus(
                reverse("turbion_dashboard_blog_post_new", kwargs={"blog": "test"}),
                http.HttpResponse.status_code
        )

    def test_edit_post(self):
        pass
