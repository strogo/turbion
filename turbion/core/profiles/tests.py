# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from turbion.core.utils.testing import BaseViewTest
from turbion.core.profiles.models import Profile

class ProfilesViewsTest(BaseViewTest):
    fixtures = ["turbion/test/profiles"]

    def test_profile_index(self):
        response = self.assertStatus(reverse("turbion_profile_index", kwargs={"profile_user": "test"}))


class ProfileCreation(TestCase):
    def test_creation(self):
        user = User.objects.create_user("test", "test@test.test")

        self.assertEqual(Profile.objects.count(), 1)

        profile = Profile.objects.get(username="test")

        self.assertEqual(profile.email, "test@test.test")
        self.assertEqual(profile.nickname, "test")
