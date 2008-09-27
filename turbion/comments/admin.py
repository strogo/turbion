# -*- coding: utf-8 -*-
from django.contrib import admin

from turbion.comments.models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('created_on', "created_by", "status", "connection_ct", "connection_id", "postprocesor" )
    list_per_page = 25

    date_hierarchy = 'created_on'
    list_filter = ('status',)

admin.site.register(Comment, CommentAdmin)
