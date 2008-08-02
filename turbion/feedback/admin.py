# -*- coding: utf-8 -*-
from django.contrib import admin

from turbion.feedback.models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    pass

admin.site.register(Feedback, FeedbackAdmin)
