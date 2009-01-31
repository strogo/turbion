# -*- coding: utf-8 -*-
from turbion import admin
from turbion.core.staticpages.models import Page

class PageAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'slug', 'blog', 'created_on', 'edited_on', 'created_by',
        'status', 'text_postprocessor'
    )
    list_filter = ('blog', 'status')
    list_display_links = ('title',)

    def save_model(self, request, page, form, change):
        if not change:
            page.edited_by = request.user

        page.save()

admin.site.register(Page, PageAdmin)
