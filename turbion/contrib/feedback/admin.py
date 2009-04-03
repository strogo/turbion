from django import forms

from django.contrib import admin
from turbion.contrib.feedback.models import Feedback
from turbion.core.profiles import get_profile

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_on', 'created_by', 'status')
    list_filter = ('status',)
    list_select_related = ('created_by',)

    def save_model(self, request, feedback, form, change):
        if not change:
            feedback.edited_by = get_profile(request)

        feedback.save()

admin.site.register(Feedback, FeedbackAdmin)
