from django.contrib import admin

from turbion.bits.whitelist.models import Source

class SourceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Source, SourceAdmin)
