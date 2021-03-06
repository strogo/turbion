from django.db import models
from django.utils.translation import ugettext_lazy as _

from turbion.bits.utils.models import FilteredManager
from turbion.bits.utils.enum import NamedEnum

class Alias(models.Model):
    user_agents = NamedEnum(
        feedburner=("(feedburner|feedvalidator)", "feedburner bot"),
    )

    status_codes = NamedEnum(
        redirect =(302, "redirect"),
        permanent=(301, "permanent redirect")
    )

    from_url    = models.CharField(max_length=250, unique=True, verbose_name=_("from url"))
    to_url      = models.CharField(max_length=250, verbose_name=_("to url"))
    status_code = models.PositiveIntegerField(choices=status_codes, verbose_name=_("status code"),
                                              default=status_codes.permanent)

    exclude_user_agent = models.CharField(max_length=250, choices=user_agents,
                                          null=True, blank=True,
                                          verbose_name=_("exclude user agent"))

    is_active   = models.BooleanField(default=True, verbose_name=_("is active"))

    objects = models.Manager()
    active  = FilteredManager(is_active=True)

    class Meta:
        app_label = 'turbion'
        db_table = "turbion_alias"

        verbose_name = _("alias")
        verbose_name_plural = _("aliases")
