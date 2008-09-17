# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from turbion.utils.testing import BaseViewTest
from turbion.profiles.models import Profile

class ProfilesViewsTest(BaseViewTest):
    def setUp(self):
        self.profile = Profile.objects.create_profile("daev", email="foobar@dot.com", password="foobar")

    def test_profile_view(self):
        response = self.assertStatus(reverse("profile_index", kwargs={"profile_user": self.profile.username}))
