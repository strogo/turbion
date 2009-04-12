from django import forms
from django.utils.translation import ugettext_lazy as _

from turbion.core.blogs.models import Comment
from turbion.core.profiles.forms import combine_profile_form_with

class _CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text", "text_filter")

    notify = forms.BooleanField(initial=False, required=False, label=_("notify"))

class CommentForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        self.__class__ = combine_profile_form_with(
            _CommentForm,
            request=request,
            field="created_by",
            filter_field="text_filter"
        )

        self.__class__.__init__(self, *args, **kwargs)

    def clean_notify(self):
        notify = self.cleaned_data["notify"]
        if notify and ("email" in self.fields and not self.cleaned_data.get("email")):
            raise forms.ValidationError(_("You have to provide email address"
                                            " to recieve notifications"))
        return notify

class SearchForm(forms.Form):
    query = forms.CharField(required=True, label=_('search'))
