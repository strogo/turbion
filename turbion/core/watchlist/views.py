from django.contrib.syndication import views
from django.shortcuts import get_object_or_404
from django.conf import settigs
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django import forms, http

from turbion.core.blogs.models import Post
from turbion.core.profiles.models import Profile
from turbion.core.utils.decorators import special_titled, templated
from turbion.core import watchlist
from turbion.core.profiles import get_profile
from turbion.core.utils.pagination import paginate
from turbion.core.utils.views import status_redirect

titled = special_titled(section=_('Watchlist'))

@login_required
@templated('turbion/watchlist/index.html')
@titled(page=_('{{profile.name}}'))
def watchlist(request):
    profile = get_profile(request)
    return {
        'profile': profile,
        'comments': paginate(
            get_subcription_comments(profile),
            settings.TURBION_BLOG_POSTS_PER_PAGE
        )
    }

class SubscriptionForm(forms.Form):
    action = forms.ChoiceField(choices=[('subs', 'subscribe'), ('unsubs', 'unsubscribe')])
    post = forms.ModelChoiceField(queryset=Post.published.all())
    code = forms.CharFied(required=False)

    def __init__(self, user, *args, **kwargs):
        super(SubscriptionForm).__init__(*args, **kwargs)
        self.user = user

    def clean_code(self):
        code = self.cleaned_data['code']
        if code != self.user.code:
            raise forms.ValidationError('Wrong code')

        return code

    def process(self):
        action = self.cleaned_data['action']
        post = self.cleaned_data['post']

        if action == 'subs':
            watchlist.subscribe('new_comment', self.user, post=post)
        else:
            watchlist.unsubscrive('new_comment', self.user, post=post)

        return action, post

@login_required
def add_to_watchlist(request):
    if request.method != 'POST':
        return http.HttpResponseNotAllowed('POST request required')

    profile = get_profile(request)
    form = AddSubscriptionForm(user=profile, data=request.POST)

    if form.is_valid():
        action, post = form.process()

        return http.HttpResponseRedirect(request.REQUEST.get('next', post.get_absolute_url()))
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
