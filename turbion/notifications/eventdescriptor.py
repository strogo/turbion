# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.template import loader
from django.template import Context, Template, TemplateDoesNotExist
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.contrib.contenttypes.models import ContentType
from django.dispatch import dispatcher
from django.db import models
from django.utils.functional import curry

from turbion.notifications.models import Event, Connection
from turbion.visitors.models import User

class EventMeta( object ):
    def __init__( self, name, link = lambda x: x, to_object = False ):
        self.name = name
        self.link = link
        self.to_object = to_object

def enshure_user( func ):
    def _decorator( cls, user, *args, **kwargs ):
        from turbion.profiles.models import Profile
        from turbion.visitors.models import Visitor

        if isinstance( user, User ):
            pass
        elif isinstance( user, ( Profile, Visitor ) ):
            user = User.objects.get_or_create_for( user )[ 0 ]
        else:
            raise ValueError, "User object must be Profile or Visitor instance"

        return func( cls, user, *args, **kwargs )
    return _decorator

class EventSpot( type ):
    def __new__( cls, name, bases, attrs ):
        try:
            EventDescriptor
        except NameError:
            cls.descriptors = {}

            return super( EventSpot, cls ).__new__(cls, name, bases, attrs)

        if "Meta" in attrs:
            Meta = attrs.pop( "Meta" )

            link       = getattr( Meta, "link", lambda x: x )
            trigger    = getattr( Meta, "trigger", None )
            event_name = getattr( Meta, "name", name )
            to_object  = getattr( Meta, "to_object", False )

            meta = EventMeta( link = link, name = event_name, to_object = to_object )
        else:
            meta = EventMeta( name = name )
            trigger = None

        attrs[ "meta" ] = meta

        t = type.__new__( cls, name, bases, attrs )

        descriptor = "%s.%s" % ( t.__module__, name )

        t.meta.descriptor = descriptor
        cls.descriptors[ descriptor ] = t

        if trigger:
            if isinstance( trigger, (tuple,list) ):
                sender = trigger[ 0 ]
                signal = trigger[ 1 ]
            else:
                sender = dispatcher.Any
                signal = trigger

            dispatcher.connect( t.fire,
                                sender = sender,
                                signal = signal )

        return t

class EventDescriptor( object ):
    __metaclass__ = EventSpot

    name = "Some event"

    @classmethod
    def _create_connection(self, obj = None):
        if obj:
            return { "connection_ct" : ContentType.objects.get_for_model( obj.__class__ ),
                     "connection_id" : obj._get_pk_val() }
        else:
            return { "connection_ct" : None,
                     "connection_id" : None }

    @classmethod
    @enshure_user
    def subscribe(cls, user, obj = None):
        try:
            con = Connection.objects.get(user = user,
                                          event = cls._get_event(),
                                          **cls._create_connection(obj))
        except Connection.DoesNotExist:
            con = Connection.objects.create(user = user,
                                             event = cls._get_event(),
                                             **cls._create_connection(obj))

    @classmethod
    @enshure_user
    def unsubscribe(cls, user, obj = None):
        try:
            con = Connection.objects.get( user = user,
                                          event = cls._get_event(),
                                          **cls._create_connection( obj ) )
            con.delete()
        except Connection.DoesNotExist:
            pass

    @classmethod
    @enshure_user
    def has_subscription(cls, user, obj = None):
        try:
            con = Connection.objects.get( user = user,
                                          event = cls._get_event(),
                                          **cls._create_connection( obj ) )
            return True
        except Connection.DoesNotExist:
            return False

    @classmethod
    def fire(cls, instance=None, *args, **kwargs):
        try:
            obj = cls.meta.link.im_func( instance )
        except AttributeError:
            obj = cls.meta.link( instance )

        recipients = cls._get_recipients( obj )

        if not len(recipients):
            return

        domain = Site.objects.get_current().domain
        from_email = "notifications@%s" % domain

        event = cls._get_event()

        try:
            name = event.template
            if not name:
                name = cls.meta.descriptor.replace( ".", "/" ) + ".html"
            template = loader.get_template(name)
        except TemplateDoesNotExist, e:
            return "fail: %s" % e

        title = Template(event.subject_title)

        emails = set()

        for r in recipients:
            email = r.email

            if cls.allow_recipient(obj=obj, recipient=r, *args, **kwargs) and email and email not in emails:
                emails.add(email)

                base_url =" http://%s" % domain

                context = Context({"event"    : event,
                                   "recipient": r,
                                   "base_url" : base_url,
                                   "obj": obj,
                                   "unsubscribe_url": "%s%s" % (base_url, cls.get_unsubscribe_url(r, obj))})

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

    @classmethod
    def _get_recipients( cls, obj = None ):
        event = cls._get_event()
        if obj and not cls.meta.to_object:
            obj = None
        conn = cls._create_connection( obj )
        print conn, Connection.objects.filter(event=event, **conn).values_list("user", flat=True)
        users = User.objects.filter( pk__in = Connection.objects.filter(event=event,**conn ).values_list( "user", flat = True ) )

        return users

    @classmethod
    def _get_event(cls):
        event, _ = Event.objects.get_or_create( descriptor = cls.meta.descriptor )
        return event

    @classmethod
    def allow_recipient(cls, *args, **kwargs):
        return True

    @classmethod
    @enshure_user
    def get_user_hash(cls, user):
        import md5

        hash = md5.new( "%s.%s" % (user._get_pk_val(), user ) ).hexdigest()

        return hash

    @classmethod
    @enshure_user
    def get_unsubscribe_url(cls, user, obj=None):
        from django.core.urlresolvers import reverse

        url = reverse( "notifications_unsubscribe", args = ( user._get_pk_val(), cls._get_event()._get_pk_val() ) )

        if obj:
            url += "?connection_ct_id=%s&connection_id=%s" % ( ContentType.objects.get_for_model( obj.__class__ )._get_pk_val(),
                                                               obj._get_pk_val() )
        else:
            url += "?"

        hash = cls.get_user_hash( user )
        url += "&code=%s" % hash

        return url
