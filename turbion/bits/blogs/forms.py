from django import forms
from django.utils.translation import ugettext_lazy as _

from turbion.bits.blogs.models import Comment
from turbion.bits.profiles.forms import combine_profile_form_with


class _CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class CommentForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        self.__class__ = combine_profile_form_with(
            _CommentForm,
            request=request,
            field="created_by",
            filter_field="text_filter"
        )

        self.__class__.__init__(self, *args, **kwargs)


class SearchForm(forms.Form):
    query = forms.CharField(required=True, label=_('search'))
