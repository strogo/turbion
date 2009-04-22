from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template import loader, Context

from turbion.core.profiles.models import Profile
from turbion.core.blogs.models import Post
from turbion.core.utils.urls import uri_reverse

class Event(models.Model):
    name = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=150)

    is_active = models.BooleanField(default=True)

    default_subject_template = "turbion/watchlist/default_subject.html"
    default_body_template = "turbion/watchlist/default_body.html"

    def __unicode__(self):
        return self.name

    def render_subject(self, context):
        return loader.select_template(
            ["turbion/watchlist/%s_subject.html" % self.name, self.default_subject_template]
        ).render(Context(context))

    def render_body(self, context):
        return loader.select_template(
            ["turbion/watchlist/%s_body.html" % self.name, self.default_body_template]
        ).render(Context(context))

    class Meta:
        db_table = 'turbion_watchlist_event'
        app_label = 'turbion'
        verbose_name = _('event')
        verbose_name_plural = _('events')

class Subscription(models.Model):
    user = models.ForeignKey(Profile)
    event = models.ForeignKey(Event)

    date = models.DateTimeField(default=datetime.now)

    post = models.ForeignKey(Post, null=True, blank=True)

    email = models.BooleanField(default=True, db_index=True)

    def get_unsubscribe_url(self):
        from django.utils.http import urlencode

        url = uri_reverse(
            "turbion_watchlist_unsubscribe",
            args=(self.user.pk,)
        )

        url += '?' + urlencode({
            'post': self.post.pk,
            'action': 'unsubs',
            'code': self.user.get_code()
        })

        return url

    class Meta:
        db_table = 'turbion_subscription'
        app_label = 'turbion'
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')

class Message(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.now)

    body = models.TextField()
    content_type = models.CharField(max_length=50, blank=True)

    def send(self):
        domain = Site.objects.get_current().domain
        from_email = settings.TURBION_NOTIFACTIONS_FROM_EMAIL % {"domain": domain}

        msg = EmailMessage(
            self.subject,
            self.body,
            from_email,
            [self.email]
        )

        if self.content_type:
            msg.content_subtype = self.content_type

        msg.send()

    class Meta:
        ordering = ['date']
        app_label = "turbion"
