# -*- coding: utf-8 -*-
from django.template import loader
from django.template import Context, Template
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.db import models
from django.conf import settings
from django.utils.encoding import force_unicode

from turbion.utils import memoize
from turbion.utils.descriptor import to_descriptor
from turbion.notifications.models import Event, Connection
from turbion.profiles.models import Profile

class EventMeta(object):
    def __init__(self, options):
        self.name = getattr(options, "name", "Some event")
        self.to_object = getattr(options, "to_object", None)
        self.trigger = getattr(options, "trigger", None)
        self.description = getattr(options, "description", None)
        self.content_type = getattr(options, "content_type", None)

class EventSpot(type):
    def __new__(cls, name, bases, attrs):
        try:
            EventDescriptor
        except NameError:
            cls.descriptors = {}

            return super(EventSpot, cls).__new__(cls, name, bases, attrs)

        new_event = super(EventSpot, cls).__new__(cls, name, bases, attrs)
        descriptor = "%s.%s" % (new_event.__module__, name)

        new_event.meta = EventMeta(attrs.get("Meta", None))
        new_event.meta.descriptor = descriptor

        instance = new_event()

        cls.descriptors[descriptor] = instance
        new_event.instance = instance

        trigger = new_event.meta.trigger

        if trigger:
            if isinstance(trigger, (tuple, list)):
                sender = trigger[0]
                signal = trigger[1]
            else:
                sender = None
                signal = trigger

            signal.connect(instance.fire,
                           sender=sender,
                    )

        return new_event

class EventDescriptor(object):
    __metaclass__ = EventSpot

    default_template = "notifications/default.html"
    default_subject = "{{descriptor}} notification"

    def __unicode__(self):
        return force_unicode(self.meta.name)

    def get_connection(self, instance):
        return instance

    def _create_connection(self, obj=None):
        if obj:
            return {
                "connection_dscr": to_descriptor(obj.__class__),
                "connection_id": obj._get_pk_val()
            }
        else:
            return {
                "connection_dscr": None,
                "connection_id": None
            }

    def subscribe(self, user, obj=None):
        try:
            con = Connection.objects.get(user=user,
                                        event=self._get_event(),
                                        **self._create_connection(obj))
        except Connection.DoesNotExist:
            con = Connection.objects.create(user=user,
                                            event=self._get_event(),
                                            **self._create_connection(obj))

    def unsubscribe(self, user, obj=None):
        try:
            con = Connection.objects.get(
                                user=user,
                                event=self._get_event(),
                                **self._create_connection(obj)
                            )
            con.delete()
        except Connection.DoesNotExist:
            pass

    def has_subscription(self, user, obj=None):
        try:
            con = Connection.objects.get(user=user,
                                         event=self._get_event(),
                                         **self._create_connection(obj))
            return True
        except Connection.DoesNotExist:
            return False

    def _get_template(self):
        event = self._get_event()

        name = event.template
        if not name:
            name = self.meta.descriptor.replace(".", "/") + ".html"

        return loader.select_template([name, self.default_template])

    def fire(self, instance=None, *args, **kwargs):
        obj = self.get_connection(instance)

        recipients = self._get_recipients(obj)

        if not len(recipients):
            return "no recipients"

        domain = Site.objects.get_current().domain
        from_email = settings.TURBION_NOTIFACTIONS_FROM_EMAIL % {"domain": domain}

        event = self._get_event()

        body_template = self._get_template()
        title_template = Template(event.subject_title or self.default_subject)

        emails = set()

        for r in recipients:
            email = r.email

            if self.allow_recipient(obj=obj, recipient=r, *args, **kwargs)\
                and email\
                and email not in emails:

                emails.add(email)

                base_url = "http://%s" % domain

                context = Context({
                    "event": event,
                    "recipient": r,
                    "descriptor": self,
                    "base_url": base_url,
                    "obj": obj,
                    "unsubscribe_url": "%s%s" % (base_url, self.get_unsubscribe_url(r, obj))
                })

                context.update(kwargs)

                msg = EmailMessage(
                    title_template.render(context),
                    body_template.render(context),
                    from_email,
                    [email]
                )

                if self.meta.content_type:
                    msg.content_subtype = self.meta.content_type

                try:
                    msg.send()
                except Exception:
                    continue

        return "success"

    def _get_recipients(self, obj=None):
        event = self._get_event()
        if obj and not self.meta.to_object:
            obj = None
        conn = self._create_connection(obj)

        users = [con.user for con in\
            Connection.objects.filter(event=event, **conn).select_related("user")
        ]

        return users

    #@memoize
    def _get_event(self):
        event, _ = Event.objects.get_or_create(descriptor=self.meta.descriptor)
        return event

    def allow_recipient(self, *args, **kwargs):
        return True

    def get_user_hash(self, user):
        import md5

        hash = md5.new("%s.%s" % (user._get_pk_val(), user)).hexdigest()

        return hash

    def get_unsubscribe_url(self, user, obj=None):
        from django.utils.http import urlencode
        from django.core.urlresolvers import reverse

        event = self._get_event()# to ensure that event model object createad

        hash = self.get_user_hash(user)

        url = reverse(
                "turbion_notifications_unsubscribe",
                args=(user._get_pk_val(), self._get_event()._get_pk_val())
        )

        url += "?"
        if obj:
            url += urlencode({
                    "connection_dscr": to_descriptor(obj.__class__),
                    "connection_id": obj._get_pk_val(),
                    "code":  hash
            })

        return url
