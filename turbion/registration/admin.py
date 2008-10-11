# -*- coding: utf-8 -*-
from turbion import admin
from turbion.registration.models import ForbiddenName, Offer

class ForbiddenNameAdmin(admin.ModelAdmin):
    pass

admin.site.register(ForbiddenName, ForbiddenNameAdmin)

class OfferAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "date", "code", "data")
    list_filter = ("code",)

admin.site.register(Offer, OfferAdmin)
