# -*- coding: utf-8 -*
from django.core import mail
from django import http
from django.conf import settings
from django.core.urlresolvers import reverse

from turbion.core.profiles.models import Profile
from turbion.contrib.feedback.models import FeedbackAdd
from turbion.core.utils.testing import BaseViewTest

class FeedbackPageTest(BaseViewTest):
    fixtures = [
        "turbion/test/profiles", "turbion/test/blogs"
    ]

    def setUp(self):
        self.profile = Profile.objects.all()[0]

        self.login()

        FeedbackAdd.manager.subscribe(self.profile)

    def test_submit_feedback(self):
        url = reverse("turbion_feedback")

        self.assertStatus(
            url,
            http.HttpResponse.status_code
        )

        data = {
           "subject": "Test subject",
           "text": "some feedback"
        }

        self.assertStatus(
            url,
            http.HttpResponseRedirect.status_code,
            data=data,
            method="post"
        )

        self.assertEqual(len(mail.outbox), 1)
