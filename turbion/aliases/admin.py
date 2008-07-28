# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.contrib import admin

from turbion.aliases.models import Alias

class AliasAdmin(admin.ModelAdmin):
    list_display = ("from_url", "to_url")

admin.site.register(Alias, AliasAdmin)
