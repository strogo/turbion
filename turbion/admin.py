# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import ModelAdmin

class TurbionAdminSite(admin.AdminSite):
    def inject(self, other_site):
        other_site._registry.update(
            self._registry
        )

contrib_site = site = TurbionAdminSite()

if settings.TURBION_CONTRIB_GLOBAL_ADMIN:
    contrib_site = admin.site
