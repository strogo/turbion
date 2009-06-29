from django.contrib import admin

from turbion.bits.openid.models import Trust

class TrustAdmin(admin.ModelAdmin):
    list_display = ('url', 'date',)

admin.site.register(Trust, TrustAdmin)
