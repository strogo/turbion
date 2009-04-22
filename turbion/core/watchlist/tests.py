from django.core import mail
from django import http
from django.conf import settings

from turbion.core import watchlist
from turbion.core.watchlist.models import Message
from turbion.models import Post, Comment, Profile
from turbion.core.utils.testing import BaseViewTest

def queue_len():
    return Message.objects.count()

class WatchlistTest(BaseViewTest):
    fixtures = ['turbion/test/profiles', 'turbion/test/blogs']

    def setUp(self):
        self.post = Post.objects.all()[0]

    def test_new_comment(self):
        watchlist.subscribe(
            self.user,
            'new_comment',
            self.post,
            email=True
        )

        comment = Comment.objects.create(
            post=self.post,
            created_by=self.user,
            text="text comment text"
        )
        watchlist.emit_event('new_comment', post=self.post, comment=comment)

        self.assertEqual(queue_len(), 1)

    if 'turbion.contrib.feedback' in settings.INSTALLED_APPS:
        def test_new_feedback(self):
            from turbion.contrib.feedback.models import Feedback

            watchlist.subscribe(
                self.user,
                'new_feedback',
                email=True
            )

            feedback = Feedback.objects.create(
                created_by=self.user,
                subject='test',
                text='test text'
            )
            watchlist.emit_event('new_feedback', feedback=feedback)

            self.assertEqual(queue_len(), 1)

    def _test_unsubscribe(self):
        self.login()

        AnimalAdd.manager.subscribe(self.profile, self.owner)

        url, data = AnimalAdd.manager.get_unsubscribe_url(self.profile, self.owner).split("?")

        response = self.client.get(url, dict(d.split('=') for d in data.split('&')))

        self.assertEqual(response.status_code, http.HttpResponseRedirect.status_code)

        self.assert_(not AnimalAdd.manager.has_subscription(self.profile, self.owner))
