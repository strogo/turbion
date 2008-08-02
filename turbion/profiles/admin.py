# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.contrib import admin

from turbion.profiles.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email", "birth_date", "gender")
    list_per_page = 25
    list_filter = ("gender", "country", "city")

admin.site.register(Profile, ProfileAdmin)
