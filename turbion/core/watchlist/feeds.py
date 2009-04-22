from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django import http

from turbion.core.blogs.models import Comment
from turbion.profiles.models import Profile
from turbion.core.blogs.feeds import CommentsFeedAtom
from turbion.core.watchlist.models import Subscription
from turbion.core import watchlist

class UserFeed(CommentsFeedAtom):
    link = None

    def get_object(self, bits):
        if len(bits) == 1:
            return Profile.objects.get(pk=bits[0])
        raise http.Http404

    def title(self, user):
        return gen_title({
            "page": _('Watchlist'),
            "section": _('For %s') % user.name
        })

    def subtitle(self, user):
        return _('Watchlist for %s') % user.name

    def items(self, user):
        return watchlist.get_subcription_comments(user)[:50]
