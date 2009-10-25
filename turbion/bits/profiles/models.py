from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from django.utils.encoding import force_unicode

from datetime import date

from turbion.bits.markup.fields import MarkupField
from turbion.bits.utils.models import FilteredManager

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

    def create_guest_profile(self, nickname=None, email=None, ip=None, host=None, **kwargs):
        if kwargs.get('openid') and nickname is None:
            nickname = kwargs['openid']
        profile = self.create_user(username=self.generate_username([nickname, email]),
                                   email=email and email or "",
                                   password=None)

        profile.nickname = nickname
        profile.ip = ip
        profile.__dict__.update(kwargs)
        profile.save()

        return profile

    def has_superuser(self):
        return self.filter(
            is_staff=True, is_superuser=True, is_active=True, trusted=True
        ).count() != 0

class Profile(User):
    nickname = models.CharField(max_length=150, null=True, verbose_name =_('nickname'))
    ip = models.IPAddressField(null=True, blank=True, verbose_name =_('IP'))

    # True when user is quest but trusted and have
    # right as registered user when posting comment
    trusted = models.BooleanField(default=False, verbose_name=_("trusted"), db_index=True)

    filter = MarkupField(verbose_name=_('filter'))

    openid = models.CharField(max_length=255, verbose_name=_('openid'), blank=True,
                              default='', db_index=True)

    objects = ProfileManager()

    @property
    def full_name(self):
        return (self.first_name and self.last_name) and '%s %s' % (self.first_name, self.last_name) or ''

    @property
    def name(self):
        for value in (self.nickname, self.full_name, self.openid):
            if value:
                return value

        return self.username

    def is_trusted(self):
        return self.trusted

    def __unicode__(self):
        return self.name

    def get_code(self):
        import md5
        return md5.new(".".join(map(force_unicode, [self.pk, self.username, self.email]))).hexdigest()

    def has_subscription(self, event, post=None):
        from turbion.bits.watchlist.models import Subscription

        return bool(Subscription.objects.filter(user=self, event__name=event, post=post).count())

    @models.permalink
    def get_absolute_url(self):
        return ("turbion_profile", (self.username,))

    @models.permalink
    def get_watchlist_atom_url(self):
        return ('turbion_watchlist_feed', ('atom/%s/' % self.pk,))

    class Meta:
        app_label           = "turbion"
        verbose_name        = _('profile')
        verbose_name_plural = _('profiles')
        db_table            = "turbion_profile"

def create_profile_for_user(sender, instance, created, *args, **kwargs):
    from turbion.bits.profiles.models import Profile
    try:
        Profile.objects.get(user_ptr=instance)
    except Profile.DoesNotExist:
        p = Profile()
        p.__dict__.update(instance.__dict__)
        p.nickname = p.username
        p.save()

signals.post_save.connect(create_profile_for_user, sender=User)
