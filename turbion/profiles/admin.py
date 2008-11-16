# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.conf import settings

from turbion import admin
from turbion.profiles.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display  = (
        "username", "nickname", "email", "last_visit", "site",
        "is_confirmed", "ip", "host", "birth_date", "gender", "postprocessor"
    )
    list_per_page = 50
    list_display_links = ("username", "nickname")
    list_filter   = ("is_confirmed", "is_superuser", "is_staff", "country", "city", "gender", "postprocessor")
    search_fields = ("username", "nickname", "email", "site")

admin.site.register(Profile, ProfileAdmin)
