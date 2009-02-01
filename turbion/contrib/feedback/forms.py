# -*- coding: utf-8 -*-
from django import forms

from turbion.core.profiles.forms import combine_profile_form_with
from turbion.contrib.feedback.models import Feedback

class _FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("subject", "text")

class FeedbackForm(forms.Form):
    def __init__(self, request, blog, *args, **kwargs):
        self.__class__ = combine_profile_form_with(
                                _FeedbackForm,
                                request=request,
                                field="created_by",
                                need_captcha=False
                        )

        self.__class__.__init__(self, *args, **kwargs)
