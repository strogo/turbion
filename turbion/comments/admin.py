# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.contrib import admin

from turbion.comments.models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('created_on', "created_by", "text", "status", "connection_ct", "action_delete" )
    list_per_page = 25

    date_hierarchy = 'created_on'
    list_filter = ('status',)

admin.site.register(Comment, CommentAdmin)
