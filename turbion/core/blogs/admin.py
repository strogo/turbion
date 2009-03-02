from django import forms
from django.utils.text import truncate_words
from django.utils.encoding import force_unicode

from turbion import admin
from turbion.core.blogs.models import Post, Comment, Tag
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

        form.save_m2m()

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'created_on', 'post', 'status', 'created_by', 'headline',
        'text_filter',
    )
    list_per_page = 25

    date_hierarchy = 'created_on'
    list_filter = ('status',)

    def headline(self, comment):
        return truncate_words(comment.text, 5)
    headline.short_description = 'headline'

    def save_model(self, request, comment, form, change):
        if not change:
            comment.edited_by = get_profile(request)

        comment.save()

admin.site.register(Comment, CommentAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'post_count',
    )
    list_per_page = 25

admin.site.register(Tag, TagAdmin)
