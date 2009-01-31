# -*- coding: utf-8 -*-
from django import forms

from turbion import admin
from turbion.core.feedback.models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("subject", "blog", "created_on", "created_by", "status")
    list_filter = ("blog", "status",)

    def save_model(self, request, feedback, form, change):
        if not change:
            feedback.edited_by = request.user

        feedback.save()

admin.site.register(Feedback, FeedbackAdmin)
