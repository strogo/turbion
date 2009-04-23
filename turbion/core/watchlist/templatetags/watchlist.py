from django.template import Library

from turbion.core.watchlist.forms import SubscriptionForm
from turbion.core.profiles import get_profile

register = Library()

@register.inclusion_tag('turbion/watchlist/subscribe_pad.html', takes_context=True)
def watchlist_pad(context, post):
    profile = get_profile(context['request'])

    action = profile.has_subscription('new_comment', post) and 'unsubs' or 'subs'

    return {
        'action': action,
        'form': SubscriptionForm(initial={'post': post.pk, 'action': action})
    }
