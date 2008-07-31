# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django import forms
from django.utils.translation import ugettext_lazy as _

from turbion.blogs.models import Comment
from turbion.profile.forms import combine_profile_form_with

class _CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text", "notify")

class CommentForm(forms.Form):
    def __init__(self, request, *args, **kwargs ):
        self.__class__ = combine_profile_form_with(_CommentForm,
                                                 request      = request,
                                                 field        = "created_by",
                                                 need_captcha = True
                                               )

        self.__class__.__init__(self, *args, **kwargs)

    def _clean_notify(self):
        notify = self.cleaned_data["notify"]
        if "email" in self.cleaned_data:
            email = self.cleaned_data["email"]

            if notify and not email:
                raise forms.ValidationError("Для получения уведомлений должен буть указан адрес почты")#FIXME: translate
        return notify
