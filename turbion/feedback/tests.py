# -*- coding: utf-8 -*
from django.core import mail
from django import http

from turbion.blogs.utils import reverse
from turbion.blogs.models import Blog
from turbion.profiles.models import Profile
from turbion.feedback.models import FeedbackAdd
from turbion.utils.testing import BaseViewTest

class FeedbackPageTest(BaseViewTest):
    fixtures = [
        "turbion/test/profiles", "turbion/test/blogs"
    ]

    def setUp(self):
        self.profile = Profile.objects.all()[0]
        self.blog = Blog.objects.all()[0]

        self.login()

        FeedbackAdd.instance.subscribe(self.profile, self.blog)

    def test_submit_feedback(self):
        url = reverse("turbion_feedback", args=(self.blog.slug,))

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
