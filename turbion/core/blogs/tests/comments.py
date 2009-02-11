# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models
from django import http

from turbion.core.blogs.models import Comment, Post
from turbion.core.blogs.views import comment as views
from turbion.core.utils.testing import RequestFactory, BaseViewTest

class CommentsTest(BaseViewTest):
    fixtures = [
        'turbion/test/blogs',
        'turbion/test/profiles'
    ]

    def setUp(self):
        self.post = Post.objects.all()[0]
        self.client = RequestFactory()

    def _create_comment(self):
        comment = Comment(
            post=self.post,
            text="Foo bar text",
            created_by=self.user
        )
        comment.save()

        return comment

    def test_add(self):
        self.login()

        data = {
            "text": "Foo bar text",
            "notify": True,
            'text_filter': "markdown"
        }

        request = self.client.post("/foobar/", data=data)

        response = views.add_comment(
                            request,
                            next="/",
                            post=self.post
                    )

        self.assert_(isinstance(response, http.HttpResponse))
        self.assertResponseStatus(response, http.HttpResponseRedirect.status_code)

        comment = Comment.objects.get()

        self.assertEqual(comment.status, Comment.statuses.published)

        post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(post.comment_count, 1)

    def test_add_guest(self):
        data = {
            "text": "Foo bar text",
            'text_filter': "markdown",
            "notify": True,
            "nickname": "Test User",
            "email": "testuser@domain.com",
            "site": "http://domain.com/",
        }
        initial_request = self.client.get("/foobar/")
        response_dict = views.add_comment(
                    initial_request,
                    next="/",
                    post=self.post
            )
        response_dict["comment_form"].as_p()
        data.update(self.hack_captcha(initial_request))

        request = self.client.post("/foobar/", data=data)
        request.session = initial_request.session

        response = views.add_comment(
                            request,
                            next="/",
                            post=self.post
                    )

        self.assert_(isinstance(response, http.HttpResponse))
        self.assertResponseStatus(response, http.HttpResponseRedirect.status_code)

        comment = Comment.objects.get()

        self.assertEqual(comment.status, Comment.statuses.published)

    def test_edit(self):
        comment = self._create_comment()

        self.login()

        data = {
            "text": "New comment text",
            'text_filter': "markdown",
        }

        request = self.client.post("/foobar/", data=data)

        response = views.add_comment(
            request,
            next="/",
            post=self.post,
            comment=comment
        )
        self.assert_(isinstance(response, http.HttpResponse))
        self.assertResponseStatus(response, http.HttpResponseRedirect.status_code)

        comment = Comment.objects.get()

        self.assertEqual(comment.text, data["text"])

    def test_delete(self):
        comment = self._create_comment()

        request = self.client.post("/foobar/")

        response = views.delete(
            request,
            comment_id=comment.id
        )
        self.assert_(isinstance(response, http.HttpResponse))
        self.assertResponseStatus(response, http.HttpResponseRedirect.status_code)

        self.assertEqual(Comment.objects.count(), 0)
