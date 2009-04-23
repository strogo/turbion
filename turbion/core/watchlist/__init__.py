from django.contrib.sites.models import Site

from turbion.core.watchlist.models import Subscription, Event, Message

def subscribe(user, event, post=None, email=False):
    event = Event.objects.get(name=event)

    subscription, _ = Subscription.objects.get_or_create(
        event=event,
        user=user,
        post=post,
        defaults={
            'email': email
        }
    )

    return subscription

def unsubscribe(user, event, post=None):
    event = Event.objects.get(name=event)

    Subscription.objects.filter(
        event=event,
        user=user,
        post=post
    ).delete()

def emit_event(event, post=None, filter_recipient=lambda user: True, **context):
    event = Event.objects.get(name=event)

    if not event.is_active:
        return

    domain = Site.objects.get_current().domain

    subscriptions = Subscription.objects.filter(event=event, post=post, email=True)
    done = set()

    for subscription in subscriptions:
        user = subscription.user
        if user.email and user.email not in done and filter_recipient(user):
            done.add(user.email)

            base_url = "http://%s" % domain

            user_context = {
                'event': event,
                'user': user,
                'post': post,
                'subscription': subscription,
                "base_url": base_url,
            }

            user_context.update(context)

            queue_mail(
                email=user.email,
                subject=event.render_subject(user_context),
                body=event.render_body(user_context)
            )

def queue_mail(email, subject, body, content_type='html'):
    msg = Message.objects.create(
        email=email,
        subject=subject,
        body=body,
        content_type=content_type
    )

def get_subcription_comments(user):
    from turbion.core.blogs.models import Comment

    return Comment.published.filter(
        post__in=Subscription.objects.filter(user=user, post__isnull=False).values('post')
    ).select_related().order_by('-created_on')
