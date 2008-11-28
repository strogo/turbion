# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from turbion.blogs.models import Post, Blog
from turbion.profiles.models import Profile
from turbion.tags.forms import TagsField
from turbion.feedback.models import Feedback
from turbion.registration.forms import CreateProfileForm

class CreateSuperuserForm(CreateProfileForm):
    def create_profile(self, username, email, password):
        return Profile.objects.create_superuser(username, email, password)

class CreateBlogForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=Profile.objects.all(), label=_("owner"))

    class Meta:
        model = Blog
        fields = ("name", "slug")

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['blog', 'created_by', 'edited_by', 'edited_on', 'text_html']

    notify = forms.BooleanField(initial=False, required=False)

    def __init__(self, request, blog, *args, **kwargs):
        self.blog = blog

        initial = kwargs.pop("initial", {})
        initial["postprocess"] = request.user.postprocessor

        super(PostForm, self).__init__(initial=initial, *args, **kwargs)

        exclude_fields = []
        if not blog.additional_post_fields:
            exclude_fields.extend(["mood", "location", "music"])

        for f in exclude_fields:
            self.fields.pop(f)

        self.fields["tags"] = TagsField(form=self)

class BlogPrefForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ("id",)

class FeedbackEditForm(forms.ModelForm):
    class Meta:
        model = Feedback
