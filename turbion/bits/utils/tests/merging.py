from datetime import date

from django.db import models
from django.test import TestCase
from django.contrib.auth.models import User

from turbion.core.utils import merging

class MyProfile(models.Model):
    user_ptr = models.ForeignKey(User, unique=True)
    nickname = models.CharField(max_length=100)
    www = models.URLField()
    birth = models.DateField()

    class Meta:
        app_label="turbion"

class OtherProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    nickname = models.CharField(max_length=100)
    website = models.URLField()
    dob = models.DateField()

    class Meta:
        app_label="turbion"

class MyProfileLayer(merging.ModelLayer):
    model = MyProfile
    fields = ["nickname"]
    aliases = {
        "site": "www",
        "day_of_birth": "birth"
    }
    key = 'user_ptr'

class OtherProfileLayer(merging.ModelLayer):
    model = OtherProfile
    fields = ["nickname"]
    aliases = {
        "site": "website",
        "day_of_birth": "dob"
    }
    key = 'user'
    create = True

merging.track([MyProfileLayer, OtherProfileLayer])


class Merge(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "test",
            "foobar@foo.bar"
        )

        self.my_profile = MyProfile.objects.create(
            user_ptr=self.user,
            nickname="test_foo",
            www="http://foo.bar",
            birth=date.today(),
        )

    def _test_objects(self, other):
        my_profile = MyProfile.objects.get(pk=self.my_profile.pk)
        self.assertEqual(other.nickname, my_profile.nickname)
        self.assertEqual(other.website, my_profile.www)
        self.assertEqual(other.dob, my_profile.birth)

    def test_other_profile_existance(self):
        self.assertEqual(
                OtherProfile.objects.filter(user=self.user).count(),
                1
            )

        other = OtherProfile.objects.get(user=self.user)
        self._test_objects(other)

    def test_other_change(self):
        other = OtherProfile.objects.get(user=self.user)

        other.website = "http://bar.foo"
        other.save()
        self._test_objects(other)

    def test_my_change(self):
        self.my_profile.website = "http://bar.foo"
        self.my_profile.save()

        other = OtherProfile.objects.get(user=self.user)
        self._test_objects(other)
