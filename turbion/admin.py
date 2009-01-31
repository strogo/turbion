# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import ModelAdmin

class TurbionAdminSite(admin.AdminSite):
    def inject(self, other_site):
        other_site._registry.update(
            self._registry
        )

site = TurbionAdminSite()
