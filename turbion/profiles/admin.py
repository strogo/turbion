# -*- coding: utf-8 -*-
from django.contrib import admin

from turbion.profiles.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "nickname", "email", "last_login", "site", "is_confirmed", "ip", "birth_date", "gender", "postprocessor")
    list_per_page = 25
    list_filter = ("is_confirmed", "is_superuser", "is_staff", "country", "city", "gender")

admin.site.register(Profile, ProfileAdmin)
