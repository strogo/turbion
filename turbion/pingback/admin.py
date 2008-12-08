# -*- coding: utf-8 -*-
from turbion import admin
from turbion.pingback.models import Incoming, Outgoing

class IncomingAdmin(admin.ModelAdmin):
    list_display= ("target_url", "source_url", "date", "title", "finished")
    list_filter = ("descriptor",)
    list_per_page = 25

admin.site.register(Incoming, IncomingAdmin)

class OutgoingAdmin(admin.ModelAdmin):
    list_display = ("target_uri", "date", "title", "status", "rpcserver",)
    list_filter = ("descriptor", )
    list_per_page = 25

admin.site.register(Outgoing, OutgoingAdmin)
