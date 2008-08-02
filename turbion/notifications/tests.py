# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models
from django.db.models import signals
from django.core.management import call_command
from django.core import mail

from turbion.notifications import EventDescriptor
from turbion.profiles.models import Profile

class Owner(models.Model):
    name = models.CharField(max_length=50)

class Animal(models.Model):
    owner = models.ForeignKey(Owner)
    name = models.CharField(max_length=50)

class AnimalAdd(EventDescriptor):
    class Meta:
        name = "Test Event"
        trigger = (Animal, signals.post_save)
        to_object = True

    def get_connection(self, instance):
        return instance.owner

class NotifTestCase(TestCase):
    fixtures = ["profiles", "dbtemplates"]

    def setUp(self):
        self.profile = Profile.objects.get(username = "daev")

        self.owner = Owner.objects.create(name="Sam")

    def test_model_notif(self):
        AnimalAdd.instance.subscribe(self.profile, self.owner)

        anim = Animal.objects.create(owner=self.owner, name="dog")

        self.assertEqual(len(mail.outbox), 1)

    def test_model_notif_another_obj(self):
        AnimalAdd.instance.subscribe(self.profile, self.owner)

        owner = Owner.objects.create(name="Dave")
        anim = Animal.objects.create(owner=owner, name="dog")

        self.assertEqual(len(mail.outbox), 0)

    def test_unsubscribe(self):
        from django.core.urlresolvers import reverse

        AnimalAdd.instance.subscribe(self.profile, self.owner)

        url, data = AnimalAdd.instance.get_unsubscribe_url(self.profile, self.owner).split("?")

        response = self.client.get(url, dict(d.split('=') for d in data.split('&')))

        self.assertEqual(response.status_code, 200)

        self.assert_(not AnimalAdd.instance.has_subscription(self.profile, self.owner))
