from django.contrib import admin

from turbion.bits.aliases.models import Alias

class AliasAdmin(admin.ModelAdmin):
    list_display = (
        "from_url", "to_url", 'is_active', 'status_code', 'exclude_user_agent'
    )
    list_filter = ('is_active', 'status_code', 'exclude_user_agent')

admin.site.register(Alias, AliasAdmin)
