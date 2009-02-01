# -*- coding: utf-8 -*-
from django.db import models, connection
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals

from datetime import date

from turbion.core.utils.enum import Enum
from turbion.core.utils.postprocessing.fields import PostprocessField

class ProfileManager(UserManager):
    def generate_username(self, data):
        import md5
        import random

        base = "turbion_"

        hash = md5.new(repr(data)+str(random.random())).hexdigest()[:30-len(base)]

        return base + hash

    def create_profile(self, *args, **kwargs):
        return self.create_user(*args, **kwargs)

    def create_guest_profile(self, nickname, email=None, site=None, ip=None, host=None):
        profile = self.create_user(username=self.generate_username([nickname,email,site]),
                                   email=email and email or "",
                                   password=None)

        profile.nickname = nickname
        profile.site = site
        profile.name_view = Profile.names.nickname
        profile.is_confirmed = False
        profile.ip = ip
        profile.host = host
        profile.save()

        return profile

    def has_superuser(self):
        return self.filter(is_staff=True, is_superuser=True, is_active=True,
                           is_confirmed=True).count() != 0

class Profile(User):
    names = Enum(
                nickname      =_("nick"),
                full_name     =_("full name"),
                full_name_nick=_("full name with nick"),
            )
    sites = Enum(
                profile=_("profile"),
                site   =_("site"),
            )
    genders = Enum(
                male  =_('male'),
                female=_('female')
            )

    nickname = models.CharField(max_length=150, null=True, verbose_name =_('nickname'))
    ip = models.IPAddressField(null=True, blank=True, verbose_name =_('IP'))
    host = models.CharField(max_length=250,null=True, blank=True, verbose_name =_('host'))

    # False when user is guest and not confirmed his profie
    is_confirmed = models.BooleanField(default=True, verbose_name =_('confirmed'))

    # True when user is quest but trusted and have
    # right as registered user when posting comment
    trusted = models.BooleanField(default=False, verbose_name=_("trusted"))

    birth_date = models.DateField(null=True, blank=True, verbose_name=_('birth date'))
    gender = models.CharField(max_length=10, verbose_name =_('gender'), choices=genders, null=True, blank=True)

    country = models.CharField(max_length=50, verbose_name=_('country'), null=True, blank=True)
    city = models.CharField(max_length=50, verbose_name=_('city'), null=True, blank=True)

    site = models.CharField(blank=True, max_length=100, null=True, verbose_name=('site'))

    biography = models.TextField(null=True, blank=True, verbose_name=_('biography'))
    interests = models.TextField(null=True, blank=True, verbose_name=_('interests'))
    education = models.TextField(null=True, blank=True, verbose_name=_("education"))
    work = models.TextField(null=True, blank=True, verbose_name=_("work"))

    gtalk = models.EmailField(blank=True, null=True, verbose_name=_('google talk'))
    msn = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('msn id'))
    icq = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('icq uin'))
    jabber = models.CharField(max_length=75, null=True, blank=True, verbose_name=_('jabber id'))
    skype = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('skype'))

    name_view = models.CharField(max_length=20, choices=names, null=True, blank=True, verbose_name=_('name view'))
    site_view = models.CharField(max_length=20, choices=sites,
                                 default=sites.profile, null=True, blank=True,
                                verbose_name=_('site view'))
    last_visit = models.DateTimeField(null=True, blank=True, verbose_name=_('last visit'))

    postprocessor = PostprocessField()

    objects = ProfileManager()

    def is_authenticated_confirmed(self):
        return self.is_authenticated() and self.is_confirmed

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def full_name_with_nick(self):
        return "%s %s %s" % (self.first_name, self.username, self.last_name)

    @property
    def name(self):
        type_map = {
                Profile.names.nickname      : self.nickname,
                Profile.names.full_name     : self.full_name,
                Profile.names.full_name_nick: self.full_name_with_nick
        }
        return type_map.get(self.name_view, self.username)

    def update_visit(self, when):
        self.__class__._default_manager.filter(pk=self.pk).\
                                        update(last_visit=when)

    def __unicode__(self):
        return self.name

    def get_site_url(self):
        if self.is_confirmed:
            type_map = {
                Profile.sites.profile: models.permalink(
                                        lambda: (
                                            "turbion.profiles.views.profile",
                                            (),
                                            {"profile_user": self.username}
                                            )
                                        )(),
                Profile.sites.site: self.site
            }
            return type_map.get(self.site_view, self.site)
        return self.site

    def get_absolute_url(self):
        return self.get_site_url()

    class Meta:
        app_label           = "turbion"
        verbose_name        = _('profile')
        verbose_name_plural = _('profiles')
        db_table            = "turbion_profile"

def create_profile_for_user(sender, instance, created, *args, **kwargs):
    from turbion.core.profiles.models import Profile
    try:
        Profile.objects.get(user_ptr=instance)
    except Profile.DoesNotExist:
        p = Profile()
        p.__dict__.update(instance.__dict__)
        p.nickname = p.username
        p.save()

signals.post_save.connect(create_profile_for_user, sender=User)
