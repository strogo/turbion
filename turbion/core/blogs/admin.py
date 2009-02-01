# -*- coding: utf-8 -*-
from django import forms

from turbion import admin
from turbion.core.blogs.models import Post
from turbion.core.profiles import get_profile

class PostForm(forms.ModelForm):
    notify = forms.BooleanField(initial=False, required=False)

class PostAdmin(admin.ModelAdmin):
    form = PostForm
    exclude = ['created_by', 'edited_by']

    list_display       = (
        'title', 'created_by', 'created_on', 'published_on',
        'status', 'comment_count'
    )
    list_display_links = ('title',)
    list_filter        = ('status', 'created_by',)
    list_per_page      = 50
    search_fields      = (
        'title', 'created_by__username', 'created_by__nickname', 'created_by__email',
    )

    def save_model(self, request, post, form, change):
        if not change:
            post.created_by = get_profile(request)
        else:
            post.edited_by = get_profile(request)

        was_draft = True
        if change:
            was_draft = Post.objects.get(pk=post.pk).status = Post.statuses.draft

        if was_draft and post.is_published:
            post.publicate(form.cleaned_data['notify'])
        else:
            post.save()

        #form.save_tags()

admin.site.register(Post, PostAdmin)
