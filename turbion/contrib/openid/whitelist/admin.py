from django.contrib import admin

from turbion.contrib.openid.whitelist.models import Source

class SourceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Source, SourceAdmin)
