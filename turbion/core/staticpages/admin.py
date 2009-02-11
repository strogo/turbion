# -*- coding: utf-8 -*-
from turbion import admin
from turbion.core.staticpages.models import Page
from turbion.core.profiles import get_profile

class PageAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'slug', 'created_on', 'edited_on', 'created_by',
        'status', 'text_filter'
    )
    list_filter = ('status',)
    list_display_links = ('title',)

    def save_model(self, request, page, form, change):
        if not change:
            page.edited_by = get_profile(request)

        page.save()

admin.site.register(Page, PageAdmin)
