# -*- coding: utf-8 -*-
from django.db import models, connection
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from datetime import date

from pantheon.utils.enum import Enum

from turbion.roles.models import Role, Capability

class ProfileManager(UserManager):
    def generate_username(self, data):
        import md5
        import random

        base = "turbion_"

        hash = md5.new(repr(data)+str(random.random())).hexdigest()[:30-len(base)]

        return base + hash

    def create_guest_profile(self, nickname, email=None, site=None):
        profile = self.create_user(username=self.generate_username([nickname,email,site]),
                                   email=email and email or "",
                                   password=None)

        profile.nickname = nickname
        profile.site = site
        profile.name_view = Profile.names.nickname
        profile.save()

        return profile

    def has_superuser(self):
        return self.filter(is_staff=True, is_superuser=True, is_active=True, is_confirmed=True).count() != 0

class Profile(User):
    names = Enum(nickname      =_("nick"),
                 full_name     =_("full name"),
                 full_name_nick=_("full name with nick"),
                )
    genders = Enum(male  =_('male'),
                   female=_('female')
                )

    nickname = models.CharField(max_length=150, null=True)
    ip = models.IPAddressField(null=True)
    is_confirmed = models.BooleanField(default=False)

    birth_date = models.DateField(null=True, blank=True, verbose_name=_('birth date'))
    gender = models.CharField(max_length=10, verbose_name =_('gender'), choices=genders, null=True, blank=True)

    country = models.CharField(max_length=50, verbose_name=_('country'), null=True, blank=True)
    city = models.CharField(max_length=50, verbose_name=_('city'), null=True, blank=True)

    site = models.CharField(blank=True, max_length=100, null=True, verbose_name=('site'))

    biography = models.TextField(null=True, blank=True, verbose_name=_('biography'))
    interests = models.TextField(null=True, blank=True, verbose_name=_('interests'))
    education = models.TextField(null=True, blank=True, verbose_name=_("education"))
    work = models.TextField(null=True, blank=True, verbose_name=_("work"))

    icq = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('icq uin'))
    jabber = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('jabber id'))
    skype = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('skype'))

    name_view = models.CharField(max_length=10, choices=names, null=True, blank=True)

    roles = models.ManyToManyField(Role, blank=True, related_name="profiles")
    capabilities = models.ManyToManyField(Capability, blank=True, related_name="profiles")

    objects = ProfileManager()

    def is_authenticated(self):
        return super(Profile, self).is_authenticated() and self.is_confirmed

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def full_name_with_nick(self):
        return "%s %s %s" % (self.first_name, self.username, self.last_name)

    @property
    def name(self):
        type_map = {Profile.names.nickname      : self.nickname,
                    Profile.names.full_name     : self.full_name,
                    Profile.names.full_name_nick: self.full_name_with_nick}
        return type_map.get(self.name_view, self.username)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("turbion.profiles.views.profile", (), {"profile_user": self.username})

    class Meta:
        verbose_name        = _('profile')
        verbose_name_plural = _('profiles')
        db_table            = "turbion_profile"

    @property
    def caps(self):
        if not hasattr(self, "_caps_cache"):
            self._caps_cache = set((cap.descriptor, cap.code, cap.connection) for cap in self.capabilities.all())
        return self._caps_cache

    @property
    def roles_caps(self):
        if not hasattr(self, "_roles_caps_cache"):
            caps = []
            for role in self.roles.all():
                caps.extend(role.capabilities.all())

            self._roles_caps_cache = set((cap.descriptor, cap.code, cap.connection) for cap in caps)
        return self._roles_caps_cache

    @property
    def all_caps(self):
        if not hasattr(self, "_all_caps_cache"):
            self._all_caps_cache = self.caps.union(self.roles_caps)
        return self._all_caps_cache

    def has_capability_for(self, caps, obj=None, cond="and"):
        if not isinstance(caps, (list, tuple)):
            caps = [caps]

        raw_caps = set([(cap.meta.descriptor, cap.code, obj) for cap in caps])

        cond = cond and cond.lower() or "and"

        if cond == "or":
            return len(raw_caps.intersection(self.all_caps)) > 0
        else:
            return raw_caps.issubset(self.all_caps)
