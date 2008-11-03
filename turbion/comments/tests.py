# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models
from django import http

from turbion.comments.models import Comment
from turbion.comments import views
from turbion.utils.testing import RequestFactory, BaseViewTest

class Article(models.Model):
    title = models.CharField(max_length=20)

    def get_absolute_url(self):
        return "/foobar/"

class CommentAddTest(BaseViewTest):
    fixtures = ['turbion/test/profiles']

    def setUp(self):
        self.article = Article.objects.create(title="foobar")
        self.client = RequestFactory()

    def _create_comment(self):
        comment = Comment(
            connection_dscr=self.article.__class__,
            connection_id=self.article.id,
            text="Foo bar text",
            created_by=self.user
        )
        comment.save()

        return comment

    def test_add(self):
        self.login()

        data = {
            "text": "Foo bar text",
            "notify": True
        }

        request = self.client.post("/foobar/", data=data)

        response = views.add_comment(
                            request,
                            connection=self.article
                    )
        self.assert_(isinstance(response, http.HttpResponse))
        self.assertResponseStatus(response, http.HttpResponseRedirect.status_code)

        comment = Comment.objects.get()

        self.assertEqual(comment.status, Comment.statuses.moderation)

    def test_add_guest(self):
        data = {
            "text": "Foo bar text",
            "notify": True,
            "nickname": "Test User",
            "email": "testuser@domain.com",
            "site": "http://domain.com/",
        }
        initial_request = self.client.get("/foobar/")
        response_dict = views.add_comment(
                    initial_request,
                    connection=self.article
            )
        response_dict["comment_form"].as_p()
        data.update(self.hack_captcha(initial_request))

        request = self.client.post("/foobar/", data=data)
        request.session = initial_request.session

        response = views.add_comment(
                            request,
                            connection=self.article
                    )

        self.assert_(isinstance(response, http.HttpResponse))
        self.assertResponseStatus(response, http.HttpResponseRedirect.status_code)

    def test_edit(self):
        comment = self._create_comment()

        self.login()

        data = {
            "text": "New comment text"
        }

        request = self.client.post("/foobar/", data=data)

        response = views.edit_comment(
                            request,
                            connection=self.article,
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
