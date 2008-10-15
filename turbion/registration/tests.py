# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import mail
from django.conf import settings

from turbion.registration.models import Offer
from turbion.profiles.models import Profile
from turbion.utils.testing import BaseViewTest

class ProfileMixin(object):
    username="test"
    password="test"

    def make_reg_data(self):
        return {
            "username": self.username,
            "email": "test@foo.bar",
            "password": self.password,
            "password_confirm": self.password
        }

    @property
    def profile(self):
        return Profile.objects.get(username=self.username)

    @property
    def offer(self):
        return Offer.objects.get(user=self.profile)

    def login(self):
        self.assertEqual(self.client.login(username=self.username, password=self.password), True)

class RegistrationTest(BaseViewTest, ProfileMixin):
    def setUp(self):
        pass

    def test_registration(self):
        response = self.assertStatus(reverse("turbion_registration_index"))

        data = self.make_reg_data()

        #registering user
        response = self.assertStatus(reverse("turbion_registration_index"), data=data, method="post", status=302)
        self.assertEqual(len(mail.outbox), 1)

        #try find our new user
        user = Profile.objects.get(username=data["username"])
        self.assertEqual(user.is_active, False)

        #process confirm
        response = self.assertStatus(reverse("turbion_registration_confirm"), data={"code": self.offer.code}, status=302)

        user = Profile.objects.get(username=data["username"])
        self.assertEqual(user.is_active, True)

class PasswordRestoreTest(BaseViewTest, ProfileMixin):
    fixtures = ["turbion/test/registration"]

    def test_password_restore(self):
        response = self.assertStatus(reverse("turbion_restore_password_request"))

        data = {
            "email": self.profile.email
        }

        response = self.assertStatus(reverse("turbion_restore_password_request"), data=data, method="post", status=302)
        self.assertEqual(len(mail.outbox), 1)

        response = self.assertStatus(reverse("turbion_restore_password"), data={"code": self.offer.code}, status=302)
        self.assertEqual(Offer.objects.count(), 0)

class ChangePasswordTest(BaseViewTest, ProfileMixin):
    fixtures = ["turbion/test/registration"]

    new_password="tset"

    def setUp(self):
        self.login()

    def test_good_change(self):
        data = {
            "old_password" : self.password,
            "password": self.new_password,
            "password_confirm" : self.new_password
        }

        response = self.assertStatus(
                        reverse("turbion_change_password"),
                        data=data,
                        method="post",
                        status=302
                    )

    def test_bad_change(self):
        data = {
            "old_password" : self.password+"12",
            "password": self.new_password,
            "password_confirm" : self.new_password
        }

        response = self.assertStatus(reverse("turbion_change_password"), data=data)

class ChangeEmailTest(BaseViewTest, ProfileMixin):
    fixtures = ["turbion/test/registration"]

    new_email = "test@bar.foo"

    def setUp(self):
        self.login()

    def test_good_change(self):
        data = {
            "email": self.new_email
        }

        response = self.assertStatus(reverse("turbion_change_email"), data=data, method="post", status=302)
        self.assertEqual(len(mail.outbox), 1)

        data = {
            "code": self.offer.code
        }
        response = self.assertStatus(reverse("turbion_change_email_confirm" ), data=data, status=302)

class WrongRegistrationTest(BaseViewTest, ProfileMixin):
    fixtures = ["turbion/test/registration"]

    def test_bad_username(self):
        data = self.make_reg_data()

        response = self.assertStatus(reverse("turbion_registration_index"), data=data)

    def test_bad_email(self):
        data = self.make_reg_data()

        response = self.assertStatus(reverse("turbion_registration_index"), data=data)
