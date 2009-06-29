from django.contrib import admin

from turbion.bits.pingback.models import Pingback

class PingbackAdmin(admin.ModelAdmin):
    list_display= ("target_url", "post", "source_url", "incoming", "date", "title", "finished")
    list_filter = ("incoming", "finished")
    list_per_page = 25
    list_select_related = True

admin.site.register(Pingback, PingbackAdmin)
