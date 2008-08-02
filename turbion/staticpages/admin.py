# -*- coding: utf-8 -*-
from django.contrib import admin

from turbion.staticpages.models import Page

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_by')
    list_display_links = ('title',)

admin.site.register(Page, PageAdmin)
