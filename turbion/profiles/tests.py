# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from turbion.utils.testing import BaseViewTest
from turbion.profiles.models import Profile

class ProfilesViewsTest(BaseViewTest):
    fixtures = ["turbion/test/profiles"]

    def test_profile_index(self):
        response = self.assertStatus(reverse("profile_index", kwargs={"profile_user": "test"}))
