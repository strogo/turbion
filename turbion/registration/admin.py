# -*- coding: utf-8 -*-
from turbion import admin
from turbion.registration.models import Offer

class OfferAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "date", "code", "data")
    list_filter = ("type",)

admin.site.register(Offer, OfferAdmin)
