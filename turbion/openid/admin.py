# -*- coding: utf-8 -*-
from turbion import admin
from turbion.openid.models import Identity

class IdentityAdmin(admin.ModelAdmin):
    list_display = (
        'url', 'added_on', 'user', 'last_login',
        'default', 'local'
    )
    list_per_page = 50

    date_hierarchy = 'added_on'
    list_filter = ('default', 'local')

admin.site.register(Identity, IdentityAdmin)
