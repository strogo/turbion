# -*- coding: utf-8 -*-
from django.contrib import admin

from turbion.dbtemplates.models import Template

class TemplateAdmin(admin.ModelAdmin):
    list_display = ("path", "is_active",)
    list_filter = ("is_active",)

admin.site.register(Template, TemplateAdmin)
