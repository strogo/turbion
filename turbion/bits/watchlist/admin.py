from django.conf import settings

from django.contrib import admin
from turbion.core.watchlist.models import Event, Subscription

class EventAdmin(admin.ModelAdmin):
    list_display  = ('name', 'title', 'is_active')
    list_filter   = ('is_active',)

admin.site.register(Event, EventAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display  = (
        'date', 'user', 'event', 'post', 'email'
    )
    list_per_page = 50
    list_filter   = ('email',)

admin.site.register(Subscription, SubscriptionAdmin)
