from django.db import models, connection
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals

from datetime import date

from turbion.core.utils.enum import Enum
from turbion.core.utils.markup.fields import MarkupField
from turbion.core.utils.models import GenericManager

class ProfileManager(UserManager):
    def generate_username(self, data, base="turbion_"):
        import md5
        import random
        import time

        hash = md5.new(
            repr(data) + str(random.random()) + str(time.time())
        ).hexdigest()[:30-len(base)]

        return base + hash

    def create_profile(self, *args, **kwargs):
        return self.create_user(*args, **kwargs)

    def create_guest_profile(self, nickname, email=None, site=None, ip=None, host=None, **kwargs):
        profile = self.create_user(username=self.generate_username([nickname,email,site]),
                                   email=email and email or "",
                                   password=None)

        profile.nickname = nickname
        profile.site = site
        profile.name_view = Profile.names.nickname
        profile.ip = ip
        profile.__dict__.update(kwargs)
        profile.save()

        return profile

    def has_superuser(self):
        return self.filter(
            is_staff=True, is_superuser=True, is_active=True, trusted=True
        ).count() != 0

class Profile(User):
    names = Enum(
        nickname      =_("nick"),
        full_name     =_("full name"),
        full_name_nick=_("full name with nick"),
    )
    sites = Enum(
        openid=_("openid"),
        site   =_("site"),
    )

    nickname = models.CharField(max_length=150, null=True, verbose_name =_('nickname'))
    ip = models.IPAddressField(null=True, blank=True, verbose_name =_('IP'))

    # True when user is quest but trusted and have
    # right as registered user when posting comment
    trusted = models.BooleanField(default=False, verbose_name=_("trusted"), db_index=True)

    site = models.CharField(blank=True, max_length=100, null=True, verbose_name=_('site'))

    name_view = models.CharField(max_length=20, choices=names, null=True, blank=True,
                                 verbose_name=_('name view'))
    site_view = models.CharField(max_length=20, choices=sites,
                                 default=sites.site, null=True, blank=True,
                                verbose_name=_('site view'))

    filter = MarkupField()

    openid = models.CharField(max_length=255, verbose_name=_('openid'), blank=True,
                              default='', db_index=True)

    objects = ProfileManager()

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

    def is_trusted(self):
        return self.trusted

    def __unicode__(self):
        return self.name

    def get_site_url(self):
        type_map = {
            Profile.sites.openid: self.openid,
            Profile.sites.site: self.site
        }
        return type_map.get(self.site_view, self.site or self.openid)

    def get_code(self):
        import md5
        return md5.new(".".join((self.pk, self.username, self.email))).hexdigest()

    @models.permalink
    def get_absolute_url(self):
        return ("turbion_profile", (self.username,))

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
