# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

from turbion.roles import models

class RoleSetCache( object ):
    def __init__( self ):
        self._sets = {}

    def add( self, name, set ):
        self._sets[ name ] = set

    def iteritems( self ):
        return self._sets.iteritems()

cache = RoleSetCache()

class RoleSetMeta( object ):
    def __init__( self, capabilities, roles, model ):
        self.capabilities = capabilities
        self.roles = roles

        self.model = model

class RoleSetMetaclass( type ):
    def __new__( cls, name, bases, attrs ):
        try:
            RoleSet
        except NameError:
            return super(RoleSetMetaclass, cls).__new__(cls, name, bases, attrs)

        if "Meta" in attrs:
            meta = attrs.pop( "Meta")

            model = getattr( meta, "model", None )
        else:
            model = None

        capabilities_cache = {}
        roles_cache = {}

        if "Capabilities" in attrs:
            caps = attrs.pop( "Capabilities" )

            for key, field in caps.__dict__.iteritems():
                if isinstance( field, Capability ):
                    field.code = key
                    capabilities_cache[ key ] = field

        if "Roles" in attrs:
            roles = attrs.pop( "Roles" )

            for key, field in roles.__dict__.iteritems():
                if isinstance( field, Role ):
                    field.code = key
                    roles_cache[ key ] = field

        meta = RoleSetMeta( capabilities_cache, roles_cache, model )

        attrs[ "_meta" ] = meta
        attrs[ "roles" ] = RoleManager( meta )
        attrs[ "capabilities" ] = CapabilityManager( meta )

        t = super(RoleSetMetaclass, cls).__new__( cls, name, bases, attrs )

        descriptor = "%s.%s" % ( t.__module__, name )
        meta.descriptor = descriptor

        instance = t()

        cache.add( descriptor, instance )

        return t

class RoleManager( object ):
    def __init__( self, meta ):
        self.meta = meta

    def __getattr__( self, name ):
        try:
            role = self.meta.roles[ name ]
            role.meta = self.meta
        except KeyError:
            raise AttributeError

        return role

class CapabilityManager( object ):
    def __init__( self, meta ):
        self.meta = meta

    def __getattr__( self, name ):
        try:
            cap = self.meta.capabilities[ name ]
            cap.meta = self.meta
        except KeyError:
            raise AttributeError, "No capability with name %s" % name

        return cap

class RoleSet( object ):
    __metaclass__ = RoleSetMetaclass

class Role( object ):
    def __init__( self, name, capabilities ):
        self.name = name
        self.capabilities = capabilities

    @property
    def _cap_objects( self ):
        if not hasattr( self, "_cap_objects_cache" ):
            objs = []
            for cap in self.capabilities:
                if isinstance( cap, Capability ):
                    objs.append( cap )
                elif isinstance( cap, basestring ):
                    if cap in self.meta.capabilities:
                        obj = self.meta.capabilities[ cap ]
                        obj.meta = self.meta
                        objs.append( obj )
                    else:
                        raise ValueError
                else:
                    raise TypeError
            self._cap_objects_cache = objs
        return self._cap_objects_cache

    def _create( self, profile, object = None ):
        meta = self.meta

        if meta.model:
            connection = { "connection_ct" : ContentType.objects.get_for_model( meta.model ),
                           "connection_id" : object._get_pk_val() }
        else:
            connection = {}

        role = models.Role.objects.create( code = self.code,
                                           descriptor = meta.descriptor
                                        )
        caps = []

        for cap in self._cap_objects:
            capa, _ = models.Capability.objects.get_or_create( code = cap.code,
                                                          descriptor = cap.meta.descriptor,
                                                          **connection )
            caps.append( capa )
        role.capabilities.add( *caps )

        profile.roles.add( role )

    def grant( self, profile, object = None ):
        if self.meta.model and not object:
            raise ValueError, "For `to_object=True` roles must be object persent"

        self._create( profile, object )

    def revoke( self, profile, object = None ):
        try:
            role = models.Role.objects.get_or_create( code = self.code,
                                                      descriptor = meta.descriptor )
        except models.Role.DoesNotExist:
            return
        profile.roles.remove( role )

class Capability( object ):
    def __init__( self, help_text = None ):
        self.help_text = help_text

    def _make_connection( self, object = None ):
        if self.meta.model:
            if object is None or not isinstance( object, self.meta.model ):
                raise ValueError
            connection = { "connection_ct" : ContentType.objects.get_for_model( self.meta.model ),
                           "connection_id" : object._get_pk_val() }
        else:
            connection = {}

        return connection

    def _create( self, profile, object = None ):
        connection = self._make_connection( object )

        cap, created = models.Capability.objects.get_or_create( code = self.code,
                                                                descriptor = self.meta.descriptor,
                                                                **connection )

        profile.capabilities.add( cap )

    def grant( self, profile, object = None ):
        if self.meta.model and not object:
            raise ValueError, "For model-connected roles must be object present"

        self._create( profile, object )

    def revoke( self, profile, object = None ):
        connection = self._make_connection( object )

        try:
            cap = models.Capability.objects.get( code = self.code,
                                                descriptor = self.meta.descriptor,
                                                **connection )
        except models.Capability.DoesNotExist:
            return

        profile.capabilities.remove( cap )
