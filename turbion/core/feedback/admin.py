from django import forms

from django.core import admin

from turbion.core.feedback.models import Feedback
from turbion.core.profiles import get_profile
from turbion.core.utils.antispam.admin import ActionModelAdmin

class FeedbackAdmin(ActionModelAdmin, admin.ModelAdmin):
    list_display = (
        'subject', 'created_on', 'created_by', 'status', ActionModelAdmin.action
    )
    list_filter = ('status',)
    list_select_related = True

    actions = ActionModelAdmin.batch_actions

    def save_model(self, request, feedback, form, change):
        if not change:
            feedback.edited_by = get_profile(request)

        feedback.save()

admin.site.register(Feedback, FeedbackAdmin)
