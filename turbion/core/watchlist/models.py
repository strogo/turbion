from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template import loader, Context
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.conf import settings

from turbion.core.profiles.models import Profile
from turbion.core.blogs.models import Post
from turbion.core.utils.urls import uri_reverse

class Event(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('name'))
    title = models.CharField(max_length=150, verbose_name=_('title'))

    is_active = models.BooleanField(default=True, verbose_name=_('is active'))

    default_subject_template = 'turbion/watchlist/default_subject.html'
    default_body_template = 'turbion/watchlist/default_body.html'

    def __unicode__(self):
        return self.title

    def render_subject(self, context):
        return loader.select_template(
            ['turbion/watchlist/%s_subject.html' % self.name, self.default_subject_template]
        ).render(Context(context))

    def render_body(self, context):
        return loader.select_template(
            ['turbion/watchlist/%s_body.html' % self.name, self.default_body_template]
        ).render(Context(context))

    class Meta:
        db_table = 'turbion_watchlist_event'
        app_label = 'turbion'
        verbose_name = _('event')
        verbose_name_plural = _('events')

class Subscription(models.Model):
    user = models.ForeignKey(Profile, related_name='subscriptions', verbose_name=_('user'))
    event = models.ForeignKey(Event, related_name='subscriptions', verbose_name=_('event'))

    date = models.DateTimeField(default=datetime.now, verbose_name=_('date'))

    post = models.ForeignKey(Post, null=True, blank=True, related_name='subscriptions', verbose_name=_('post'))

    email = models.BooleanField(default=False, db_index=True, verbose_name=_('email'))

    def __unicode__(self):
        return (_('%(user)s on %(event)s') % {'user': self.user, 'event': self.event}) + (self.post and _(' to `%s`') % self.post or '')

    def get_unsubscribe_url(self):
        from django.utils.http import urlencode

        url = uri_reverse(
            'turbion_watchlist_unsubscribe',
            args=(self.user.pk,)
        )

        url += '?' + urlencode({
            'post': self.post.pk,
            'action': 'unsubs',
            'code': self.user.get_code()
        })

        return url

    class Meta:
        ordering = ['-date']
        unique_together = [('event', 'user', 'post')]
        db_table = 'turbion_subscription'
        app_label = 'turbion'
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')

class Message(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.now)
    attempt = models.PositiveSmallIntegerField(default=0)

    body = models.TextField()
    content_type = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return u'`%s` to %s' % (self.subject, self.email)

    def send(self):
        try:
            domain = Site.objects.get_current().domain
            from_email = settings.TURBION_NOTIFACATION_FROM_EMAIL % {'domain': domain}

            msg = EmailMessage(
                self.subject,
                self.body,
                from_email,
                [self.email]
            )

            if self.content_type:
                msg.content_subtype = self.content_type

            msg.send()
            return True
        except Exception:
            self.attempt += 1
            self.save()
            return False

    class Meta:
        ordering = ['date']
        app_label = 'turbion'
