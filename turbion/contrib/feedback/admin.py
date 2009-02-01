# -*- coding: utf-8 -*-
from django import forms

from turbion import admin
from turbion.contrib.feedback.models import Feedback
from turbion.core.profiles import get_profile

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("subject", "created_on", "created_by", "status")
    list_filter = ("status",)

    def save_model(self, request, feedback, form, change):
        if not change:
            feedback.edited_by = get_profile(request)

        feedback.save()

admin.contrib_site.register(Feedback, FeedbackAdmin)
