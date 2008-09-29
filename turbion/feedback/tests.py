# -*- coding: utf-8 -*
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import mail

from turbion.profiles.models import Profile
from turbion.feedback.models import FeedbackAdd

CREDENTIALS = {'username': "daev", 'password': "dkflbvbhgenby"}

class FeedbackPageTest(TestCase):
    fixtures = ["profiles", "blog"]

    def setUp(self):
        self.profile = Profile.objects.all()[0]

    def test_submit_feedback(self):
        self.client.login(**CREDENTIALS)
        FeedbackAdd.instance.subscribe(self.profile)

        response = self.client.get(reverse("feedback"))
        self.assertEqual(response.status_code, 200)

        data = {}
        data["subject"] = "Test subject"
        data["text"]   = "some feedback"

        response = self.client.post(reverse("feedback"), data=data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 1)
