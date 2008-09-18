# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models

from turbion.comments.models import Comment
from turbion.comments import views

class Article(models.Model):
    title = models.CharField(max_length=20)

class CommentAddTest(TestCase):
    def setUp(self):
        self.article = Article.objects.create(title="foobar")

    def test_comment_add(self):
        pass
