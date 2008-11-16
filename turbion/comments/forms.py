# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from turbion.blogs.models import Comment
from turbion.profiles.forms import combine_profile_form_with

class _CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)

    notify = forms.BooleanField(initial=False, required=False, label=_("notify"))

class CommentForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        self.__class__ = combine_profile_form_with(
                                    _CommentForm,
                                    request=request,
                                    field="created_by",
                                    need_captcha=True,
                                    postprocessor_field="text_postprocessor"
                            )

        self.__class__.__init__(self, *args, **kwargs)

    def clean_notify(self):
        notify = self.cleaned_data["notify"]
        if notify and not self.cleaned_data.get("email"):
            raise forms.ValidationError(_("You have to provide email address"
                                            " to recieve notifications"))
        return notify
