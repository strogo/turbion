# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django import forms

from turbion.profiles.forms import combine_profile_form_with
from turbion.feedback.models import Feedback

class _FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("subject", "text")

class FeedbackForm(forms.Form):
    def __init__(self, request, blog, *args, **kwargs):
        self.__class__ = combine_profile_form_with(_FeedbackForm,
                                                 request     =request,
                                                 field       ="created_by",
                                                 need_captcha=False
                                               )

        self.__class__.__init__(self, *args, **kwargs)
