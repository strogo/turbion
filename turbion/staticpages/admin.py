# -*- coding: utf-8 -*-
from turbion import admin
from turbion.staticpages.models import Page

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_by', 'blog', 'status')
    list_filter = ('blog', 'status')
    list_display_links = ('title',)

admin.site.register(Page, PageAdmin)
