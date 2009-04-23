from django.contrib.syndication import views
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django import http
from django.core.urlresolvers import reverse

from turbion.core.blogs.models import Post
from turbion.core.profiles.models import Profile
from turbion.core.utils.decorators import special_titled, templated, paged
from turbion.core import watchlist
from turbion.core.profiles import get_profile
from turbion.core.utils.pagination import paginate
from turbion.core.utils.views import status_redirect
from turbion.core.watchlist.forms import SubscriptionForm

titled = special_titled(section=_('Watchlist'))

@paged
@login_required
@templated('turbion/watchlist/index.html')
@titled(page=_('Recent comments'))
def index(request):
    profile = get_profile(request)
    return {
        'profile': profile,
        'comments_page': paginate(
            watchlist.get_subcription_comments(profile),
            request.page,
            settings.TURBION_BLOG_POSTS_PER_PAGE
        ),
        'subscriptions': profile.subscriptions.filter(event__name='new_comment').\
                                        order_by('date').distinct()
    }

@login_required
def watchlist_action(request):
    if request.method != 'POST':
        return http.HttpResponseNotAllowed('POST request required')

    profile = get_profile(request)
    form = SubscriptionForm(user=profile, data=request.POST)

    if form.is_valid():
        action, post = form.process()

        return http.HttpResponseRedirect(request.REQUEST.get('next', reverse('turbion_watchlist')))
    return http.HttpResponseBadRequest('Post not found or bad action')

@login_required
@templated('turbion/watchlist/update.html')
@titled(page=_('Update subscriptions'))
def update_watchlist(request):
    pass

def unsubscribe(request, user_id):
    profile = get_object_or_404(Profile, pk=user_id)

    form = SubscriptionForm(user=profile, data=request.GET)
    form.fields['code'].required=True

    if form.is_valid():
        form.process()

        return status_redirect(
            request,
            title=_("Unsubscribed"),
            section=_("Watchlist"),
            message=_("You've been unsubscribed from new comment notification"),
            next="/"
        )

    return http.HttpResponseBadRequest('Post not found or bad action or bad code')
