# -*- coding: utf-8 -*-
from django.db import models

from turbion.utils.models import GenericManager
from turbion.utils.enum import NamedEnum

class Alias(models.Model):
    user_agents = NamedEnum(feedburner=("(feedburner|feedvalidator)", "feedburner bot"),
                    )

    status_codes =NamedEnum(redirect =(302, "redirect"),
                            permanent=(301, "permanent redirect")
                    )

    from_url    = models.CharField(max_length=250, unique=True)
    to_url      = models.CharField(max_length=250)
    status_code = models.PositiveIntegerField(choices=status_codes, default=status_codes.permanent)

    exclude_user_agent = models.CharField(max_length=250, choices=user_agents, null=True, blank=True)

    is_active   = models.BooleanField(default=True)

    objects = models.Manager()
    active  = GenericManager(is_active=True)

    class Meta:
        db_table = "turbion_alias"

        verbose_name = "alias"
        verbose_name_plural = "aliases"
