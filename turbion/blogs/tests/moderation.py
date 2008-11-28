# -*- coding: utf-8 -*-

from django.test import TestCase

from turbion.blogs.models import Blog, Post
from turbion.comments.models import Comment
from turbion.profiles.models import Profile

class BaseTest(object):
    fixtures = ["turbion/test/blogs", "turbion/test/profiles"]

    def setUp(self):
        self.blog = Blog.objects.all()[0]
        self.profile = Profile.objects.all()[0]

        self.blog.comments_moderation = self.moderation
        self.blog.save()

    def _add_comment(self, author):
        comment = Comment(
            created_by=author,
            text="test",
            text_postprocessor="dummy"
        )
        comment.connection = self.blog
        comment.save()

        return comment

    def test_comment_add_registered(self):
        comment = self._add_comment(self.profile)

        self.assertEqual(
            self.blog.get_comment_status(comment),
            self.registered_status
        )

    def test_comment_add_untrusted(self):
        self.profile.trusted = False
        self.profile.save()

        comment = self._add_comment(self.profile)

        self.assertEqual(
            self.blog.get_comment_status(comment),
            self.untrusted_status
        )

    def test_comment_add_guest(self):
        self.profile.trusted = False
        self.profile.is_confirmed = False
        self.profile.save()

        comment = self._add_comment(self.profile)

        self.assertEqual(
            self.blog.get_comment_status(comment),
            self.guest_status
        )

class NoneModerationTest(BaseTest, TestCase):
    moderation = Blog.moderations.none

    registered_status = Comment.statuses.published
    untrusted_status = Comment.statuses.published
    guest_status = Comment.statuses.published

class AllModerationTest(BaseTest, TestCase):
    moderation = Blog.moderations.all

    registered_status = Comment.statuses.moderation
    untrusted_status = Comment.statuses.moderation
    guest_status = Comment.statuses.moderation

class GuestsModerationTest(BaseTest, TestCase):
    moderation = Blog.moderations.guests

    registered_status = Comment.statuses.published
    untrusted_status = Comment.statuses.published
    guest_status = Comment.statuses.moderation

class UntrustedModerationTest(BaseTest, TestCase):
    moderation = Blog.moderations.untrusted

    registered_status = Comment.statuses.published
    untrusted_status = Comment.statuses.moderation
    guest_status = Comment.statuses.moderation
