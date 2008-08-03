# -*- coding: utf-8 -*-
from django.contrib import admin

from turbion.feedback.models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("subject", "blog", "created_on", "created_by", "status")
    list_filter = ("blog", "status",)

admin.site.register(Feedback, FeedbackAdmin)
