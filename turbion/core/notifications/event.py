from django.template import loader, Context, Template, TemplateDoesNotExist
from django.contrib.sites.models import Site
from django.db import models
from django.conf import settings
from django.utils.encoding import force_unicode

from turbion.core.utils import memoize
from turbion.core.utils.descriptor import to_descriptor
from turbion.core.notifications.models import Event, EventConnection, Message
from turbion.core.profiles.models import Profile

class EventManager(object):
    def __init__(self, event):
        self.event = event()

    def _create_connection(self, obj=None):
        if obj:
            return {
                "connection_dscr": to_descriptor(obj.__class__),
                "connection_id": obj.pk
            }
        else:
            return {
                "connection_dscr": None,
                "connection_id": None
            }

    def subscribe(self, user, obj=None):
        try:
            con = EventConnection.objects.get(
                user=user,
                event=self._get_event(),
                **self._create_connection(obj)
            )
        except EventConnection.DoesNotExist:
            con = EventConnection.objects.create(
                user=user,
                event=self._get_event(),
                **self._create_connection(obj)
            )

    def unsubscribe(self, user, obj=None):
        try:
            con = EventConnection.objects.get(
                user=user,
                event=self._get_event(),
                **self._create_connection(obj)
            )
            con.delete()
        except EventConnection.DoesNotExist:
            pass

    def has_subscription(self, user, obj=None):
        try:
            con = EventConnection.objects.get(
                user=user,
                event=self._get_event(),
                **self._create_connection(obj)
            )
            return True
        except EventConnection.DoesNotExist:
            return False

    #@memoize
    def _get_event(self):
        event, _ = Event.objects.get_or_create(descriptor=self.event.meta.descriptor)
        return event

    def recipients(self, obj=None):
        event = self._get_event()
        if obj and not self.event.meta.to_object:
            obj = None
        conn = self._create_connection(obj)

        users = [con.user for con in\
            EventConnection.objects.filter(event=event, **conn).select_related("user")
        ]

        return users

    def connect(self):
        trigger = self.event.meta.trigger

        if trigger:
            if isinstance(trigger, (tuple, list)):
                sender = trigger[0]
                signal = trigger[1]
            else:
                sender = None
                signal = trigger

            signal.connect(self.event_handler, sender=sender)

    def _get_template(self):
        event = self._get_event()

        name = event.template
        if not name:
            name = self.event.meta.descriptor.replace(".", "/") + ".html"

        return loader.select_template([name, self.event.default_template])

    def event_handler(self, *args, **kwargs):
        if self.event.allow_event(*args, **kwargs):
            return self.fire(*args, **kwargs)

    def fire(self, instance=None, *args, **kwargs):
        obj = self.event.get_connection(instance)

        recipients = self.recipients(obj)

        if not len(recipients):
            return "No recipients"

        domain = Site.objects.get_current().domain

        event = self._get_event()
        try:
            body_template = self._get_template()
        except TemplateDoesNotExist:
            return "No template"
        title_template = Template(event.subject_title or self.event.default_subject)

        emails = set()

        for r in recipients:
            email = r.email

            if self.event.allow_recipient(obj=obj, recipient=r, *args, **kwargs)\
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

                msg = Message.objects.create(
                    email=email,
                    subject=title_template.render(context),
                    body=body_template.render(context),
                    content_type=self.event.meta.content_type or ''
                )

        return "Success"

    def get_user_hash(self, user):
        import md5

        hash = md5.new("%s.%s" % (user.pk, user)).hexdigest()

        return hash

    def get_unsubscribe_url(self, user, obj=None):
        from django.utils.http import urlencode
        from django.core.urlresolvers import reverse

        event = self._get_event()# to ensure that event model object createad

        hash = self.get_user_hash(user)

        url = reverse(
            "turbion_notifications_unsubscribe",
            args=(user.pk, self._get_event().pk)
        )

        url += "?"
        if obj:
            url += urlencode({
                "connection_dscr": to_descriptor(obj.__class__),
                "connection_id": obj.pk,
                "code":  hash
            })

        return url

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
            return super(EventSpot, cls).__new__(cls, name, bases, attrs)

        new_event = super(EventSpot, cls).__new__(cls, name, bases, attrs)
        descriptor = "%s.%s" % (new_event.__module__, name)

        new_event.meta = EventMeta(attrs.get("Meta", None))
        new_event.meta.descriptor = descriptor

        new_event.manager = EventManager(new_event)
        new_event.manager.connect()

        return new_event

class EventDescriptor(object):
    __metaclass__ = EventSpot

    default_template = "turbion/notifications/default.html"
    default_subject = "{{descriptor}} notification"

    def __unicode__(self):
        return force_unicode(self.meta.name)

    def get_connection(self, instance):
        return instance

    def allow_event(self, *args, **kwargs):
        return True

    def allow_recipient(self, *args, **kwargs):
        return True

    @classmethod
    def to_string(cls):
        return cls.meta.name
