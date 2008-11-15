# -*- coding: utf-8 -*-
from django.template import loader
from django.template import Context, Template, TemplateDoesNotExist
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.db import models
from django.utils.functional import curry

from turbion.utils.descriptor import to_descriptor
from turbion.notifications.models import Event, Connection
from turbion.profiles.models import Profile

class EventMeta(object):
    def __init__(self, name, to_object=False):
        self.name = name
        self.to_object = to_object

class EventSpot(type):
    def __new__(cls, name, bases, attrs):
        try:
            EventDescriptor
        except NameError:
            cls.descriptors = {}

            return super(EventSpot, cls).__new__(cls, name, bases, attrs)

        if "Meta" in attrs:
            Meta = attrs.pop("Meta")

            trigger    = getattr(Meta, "trigger", None)
            event_name = getattr(Meta, "name", name)
            to_object  = getattr(Meta, "to_object", False)

            meta = EventMeta(name=event_name, to_object=to_object)
        else:
            meta = EventMeta(name=name)
            trigger = None

        attrs["meta"] = meta

        t = type.__new__(cls, name, bases, attrs)

        descriptor = "%s.%s" % (t.__module__, name)

        t.meta.descriptor = descriptor
        instance = t()

        cls.descriptors[descriptor] = instance
        t.instance = instance

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

        return t

class EventDescriptor(object):
    __metaclass__ = EventSpot

    name = "Some event"
    default_template = "notifications/default.html"

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

    def fire(self, instance=None, *args, **kwargs):
        obj = self.get_connection(instance)

        recipients = self._get_recipients(obj)

        if not len(recipients):
            return

        domain = Site.objects.get_current().domain
        from_email = "notifications@%s" % domain

        event = self._get_event()

        try:
            name = event.template
            if not name:
                name = self.meta.descriptor.replace(".", "/") + ".html"
            template = loader.get_template(name)
        except TemplateDoesNotExist, e:
            template = loader.get_template(self.default_template)

        title = Template(event.subject_title)

        emails = set()

        for r in recipients:
            email = r.email

            if self.allow_recipient(obj=obj, recipient=r, *args, **kwargs) and email and email not in emails:
                emails.add(email)

                base_url =" http://%s" % domain

                context = Context({"event"    : event,
                                   "recipient": r,
                                   "base_url" : base_url,
                                   "obj": obj,
                                   "unsubscribe_url": "%s%s" % (base_url, self.get_unsubscribe_url(r, obj))})

                context.update(kwargs)

                msg = EmailMessage( title.render(context),
                                    template.render(context),
                                    from_email,
                                    [email])
                msg.content_subtype = "html"  # Main content is now text/html
                try:
                    msg.send()
                except Exception, e:
                    return "fail: %s" % e
        return "success"

    def _get_recipients(self, obj=None):
        event = self._get_event()
        if obj and not self.meta.to_object:
            obj = None
        conn = self._create_connection(obj)

        users = Profile.objects.filter(pk__in=Connection.objects.filter(event=event, **conn).values_list("user", flat=True))

        return users

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
        from django.core.urlresolvers import reverse

        url = reverse("turbion_notifications_unsubscribe", args=(user._get_pk_val(), self._get_event()._get_pk_val()))

        #FIXME: use urlencode
        if obj:
            url += "?connection_dscr=%s&connection_id=%s" % (to_descriptor(obj.__class__), obj._get_pk_val())
        else:
            url += "?"

        hash = self.get_user_hash(user)
        url += "&code=%s" % hash

        return url
