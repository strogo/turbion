# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import connection, models

from turbion.core import capabilities
from turbion.core.profiles.models import Profile

class Animal(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        app_label = "turbion"

class AnimalCapabilities(capabilities.CapabilitySet):
    defs = dict(
        foo = "user can do bar stuff",
        bar = "user can do bar stuff"
    )

capabilities.register(AnimalCapabilities, model=Animal, name="animal.caps")

class CapabilitiesTest(TestCase):
    fixtures = ["turbion/test/profiles"]

    def setUp(self):
        self.profile = Profile.objects.all()[0]

    def test_pass_test(self):
        self.profile.grant_capability(set="animal.caps")

        self.assertEqual(self.profile.has_capability(set="animal.caps"), True)

    def test_multiple_pass(self):
        self.profile.grant_capability(set="animal.caps")

        self.assertEqual(
            self.profile.has_capability(cap=["animal.caps.foo","animal.caps.bar"]),
            True
        )

class ObjectCapabilitiesTest(TestCase):
    fixtures = ["turbion/test/profiles"]

    def setUp( self ):
        self.profile = Profile.objects.all()[0]
        self.animal = Animal.objects.create(name="dog")

    def test_grant_capabilities( self ):
        self.profile.grant_capability(set="animal.caps", instance=self.animal)

        self.assertEqual(
            self.profile.has_capability(set="animal.caps", instance=self.animal),
            True
        )

    def test_cap_grant( self ):
        self.profile.grant_capability(cap="animal.caps.foo", instance=self.animal)

        self.assertEqual(
            self.profile.has_capability(cap="animal.caps.foo", instance=self.animal),
            True
        )
