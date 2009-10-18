from django.core import mail
from django import http
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from turbion.bits import watchlist
from turbion.bits.watchlist.models import Message, Subscription
from turbion.models import Post, Comment, Profile
from turbion.bits.utils.testing import BaseViewTest

def queue_len():
    return Message.objects.count()

class WatchlistTest(BaseViewTest):
    fixtures = ['turbion/test/profiles', 'turbion/test/blogs']

    def setUp(self):
        self.post = Post.objects.all()[0]

    def _create_comment(self):
        return Comment.objects.create(
            post=self.post,
            created_by=self.user,
            text="text comment text"
        )

    def test_new_comment(self):
        watchlist.subscribe(
            self.user,
            'new_comment',
            self.post,
            email=True
        )

        comment = self._create_comment()
        watchlist.emit_event('new_comment', post=self.post, comment=comment)

        self.assertEqual(queue_len(), 1)

    def test_unsubscribe_view(self):
        sub = watchlist.subscribe(
            self.user,
            'new_comment',
            self.post,
            email=True
        )

        site = Site.objects.get_current()
        url, data = sub.get_unsubscribe_url().split("?")

        response = self.client.get(url[len('http://' + site.domain):], dict(d.split('=') for d in data.split('&')))

        self.assertEqual(response.status_code, http.HttpResponseRedirect.status_code)

        self.assertEqual(Subscription.objects.count(), 0)

    def test_feed(self):
        sub = watchlist.subscribe(
            self.user,
            'new_comment',
            self.post,
            email=True
        )
        self.create_comment()

        self.login()

        response = self.client.get(
            reverse('turbion_watchlist_feed', args=('atom/%s/' % self.user.pk,))
        )

        self.assertEqual(response.status_code, http.HttpResponse.status_code)

    def test_add_to_watchlist_view(self):
        pass
