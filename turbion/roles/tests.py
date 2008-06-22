# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.test import TestCase
from django.db import connection, models

from turbion import roles
from turbion.profiles.models import Profile

class Animal( models.Model ):
    name = models.CharField( max_length = 20 )

class SomeRoles( roles.RoleSet ):
    class Capabilities:
        foo = roles.Capability( "user can do foo stuff" )
        bar = roles.Capability( "user can do bar stuff" )

    class Roles:
        foobar = roles.Role( "Foobar user", ( "foo", "bar" ) )

class AnimalRoles( roles.RoleSet ):
    class Meta:
        model = Animal
        to_object = True

    class Capabilities:
        foo = roles.Capability( "user can do foo stuff" )
        bar = roles.Capability( "user can do bar stuff" )

    class Roles:
        foobar = roles.Role( "Foobar user", ( "foo", "bar" ) )

class AnotherRoles( roles.RoleSet ):
    class Roles:
        foobar = roles.Role( "Foobar user", ( SomeRoles.capabilities.foo, ) )

class RoleTest( TestCase ):
    def setUp( self ):
        self.profile = Profile( username = "test" )
        self.profile.save()

    def test_grant_role( self ):
        SomeRoles.roles.foobar.grant( self.profile )

        self.assertEqual( self.profile.roles.count(), 1 )

    def test_grant_capability( self ):
        SomeRoles.capabilities.foo.grant( self.profile )

        self.assertEqual( self.profile.capabilities.count(), 1 )

    def test_pass_test( self ):
        SomeRoles.capabilities.foo.grant( self.profile )

        self.assertEqual( self.profile.has_capability_for( SomeRoles.capabilities.foo ), True )

    def test_multiple_pass( self ):
        SomeRoles.roles.foobar.grant( self.profile )

        self.assertEqual( self.profile.has_capability_for( [ SomeRoles.capabilities.foo,
                                                             SomeRoles.capabilities.bar ] ), True )


class ObjectRoleTest( TestCase ):
    def setUp( self ):
        self.profile = Profile.objects.create( username = "test" )
        self.animal = Animal.objects.create( name = "dog" )

    def test_role_grant( self ):
        AnimalRoles.roles.foobar.grant( self.profile, self.animal )

        self.assertEqual( self.profile.has_capability_for( AnimalRoles.capabilities.foo, self.animal ),
                          True )

    def test_cap_grant( self ):
        AnimalRoles.capabilities.bar.grant( self.profile, self.animal )

        self.assertEqual( self.profile.has_capability_for( AnimalRoles.capabilities.bar, self.animal ),
                          True )

class CapsFromAnotherRoleSetTest( TestCase ):
    def setUp( self ):
        self.profile = Profile.objects.create( username = "test" )

    def test_grant_role( self ):
        AnotherRoles.roles.foobar.grant( self.profile )

        self.assertEqual( self.profile.roles.count(), 1 )
