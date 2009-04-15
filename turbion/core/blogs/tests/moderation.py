from django.test import TestCase

from turbion.core.blogs.models import Post, Comment
from turbion.core.profiles.models import Profile

class BaseTest(object):
    fixtures = ["turbion/test/blogs", "turbion/test/profiles"]

    def setUp(self):
        self.post = Post.objects.all()[0]
        self.profile = Profile.objects.all()[0]

        self.post.comments_moderation = self.moderation
        self.post.save()

    def _add_comment(self, author):
        comment = Comment(
            created_by=author,
            text="test",
            text_filter="dummy",
            post=self.post
        )
        comment.save()

        return comment

    def test_comment_add_registered(self):
        comment = self._add_comment(self.profile)

        self.assertEqual(
            self.post.get_comment_status(comment),
            self.registered_status
        )

    def test_comment_add_untrusted(self):
        self.profile.trusted = False
        self.profile.save()

        comment = self._add_comment(self.profile)

        self.assertEqual(
            self.post.get_comment_status(comment),
            self.untrusted_status
        )

class NoneModerationTest(BaseTest, TestCase):
    moderation = Post.moderations.none

    registered_status = Comment.statuses.published
    untrusted_status = Comment.statuses.published

class AllModerationTest(BaseTest, TestCase):
    moderation = Post.moderations.all

    registered_status = Comment.statuses.moderation
    untrusted_status = Comment.statuses.moderation

class GuestsModerationTest(BaseTest, TestCase):
    moderation = Post.moderations.guests

    registered_status = Comment.statuses.published
    untrusted_status = Comment.statuses.published

class UntrustedModerationTest(BaseTest, TestCase):
    moderation = Post.moderations.untrusted

    registered_status = Comment.statuses.published
    untrusted_status = Comment.statuses.moderation
