# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from turbion.blogs.models import Post, Blog
from turbion.profiles.models import Profile
from turbion.tags.forms import TagsField
from turbion.feedback.models import Feedback

from pantheon.supernovaforms import utils

class CreateSuperuserForm(forms.Form):
    username         = forms.CharField(required=True, label=_("username"))
    email            = forms.EmailField(required=True, label= _("email"))
    password         = forms.CharField(widget=forms.PasswordInput(), required=True, label=_("passord"))
    password_confirm = forms.CharField(widget=forms.PasswordInput(), required=True, label=_("password confirm"))

    def clean_password_confirm(self):
        password         = self.cleaned_data["password"]
        password_confirm = self.cleaned_data["password_confirm"]

        if password != password_confirm:
            raise forms.ValidationError(_("Password confirmation has been failed"))

        return password

    def create_superuser(self, username, email, password):
        u = Profile.objects.create_user(username, email, password)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save()

        return u

    def save(self):
        username = self.cleaned_data["username"]
        email    = self.cleaned_data["email"]
        password = self.cleaned_data["password"]

        user = self.create_superuser(username, email, password)

        return user

class CreateBlogForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset = Profile.objects.all())

    class Meta:
        model = Blog
        fields = ("name", "slug")

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['blog', 'created_by', 'edited_by', 'edited_on', 'text_html']

    def __init__(self, blog, *args, **kwargs):
        self.blog = blog

        super( PostForm, self ).__init__(*args, **kwargs)

        exclude_fields = []
        if not blog.additional_post_fields:
            exclude_fields.extend(["mood", "location", "music"])
        if not blog.posts_choice_postprocessor:
            exclude_fields.extend(["postprocess"])

        for f in exclude_fields:
            self.fields.pop(f)

        self.fields["tags"] = TagsField(form = self)

        if blog.posts_choice_postprocessor:
            PostForm.base_fields["postprocess"].initial = blog.posts_default_postprocessor

class BlogPrefForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ("id", "review_count",)

class LoginForm(forms.Form):
    username = forms.CharField(label = _('username'))
    password = forms.CharField(label = _('password'), widget=forms.PasswordInput())

    def clean(self):
        from django.contrib import auth

        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]

        user = auth.authenticate(username=username, password=password)
        if user:pass
            #if not user.is_active:
            #    raise forms.ValidationError( "Ваша учетная запись заблокирована. Обратитесь к администрации")
        else:
            raise forms.ValidationError(_("Illegal username or password"))
        self.cleaned_data["user"] = user
        return self.cleaned_data

class FeedbackEditForm(forms.ModelForm):
    class Meta:
        model = Feedback
