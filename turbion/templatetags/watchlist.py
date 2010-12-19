from django.template import Library

from turbion.bits.watchlist.forms import SubscriptionForm
from turbion.bits.profiles import get_profile

register = Library()

@register.inclusion_tag('turbion/watchlist/watchlist_pad.html', takes_context=True)
def watchlist_pad(context, post, labels=None):
    profile = get_profile(context['request'])

    action = profile.has_subscription('new_comment', post) and 'unsubs' or 'subs'

    return {
        'action': action,
        'labels': labels and labels.split('/'),
        'form': SubscriptionForm(initial={'post': post.pk, 'action': action})
    }
