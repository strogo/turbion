# -*- coding: utf-8 -*-
from django.utils.text import truncate_words
from django.utils.encoding import force_unicode

from turbion import admin
from turbion.core.comments.models import Comment
from turbion.core.profiles import get_profile

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'created_on', "status", "created_by",
        "target", "text_postprocessor", "headline"
    )
    list_per_page = 25

    date_hierarchy = 'created_on'
    list_filter = ('status',)

    def target(self, comment):
        return force_unicode(comment.connection)
    target.short_description = "targets"

    def headline(self, comment):
        return truncate_words(comment.text, 5)
    headline.short_description = "headline"

    def save_model(self, request, comment, form, change):
        if not change:
            comment.edited_by = get_profile(request)

        comment.save()

admin.site.register(Comment, CommentAdmin)
