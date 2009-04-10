from django import forms
from django.utils.text import truncate_words
from django.utils.encoding import force_unicode
from django.contrib import admin
from django.core.urlresolvers import reverse

from turbion.core.blogs.models import Post, Comment, Tag
from turbion.core.profiles import get_profile
from turbion.core.utils.antispam import akismet

class PostForm(forms.ModelForm):
    notify = forms.BooleanField(initial=False, required=False)

class PostAdmin(admin.ModelAdmin):
    form = PostForm
    exclude = ['created_by', 'edited_by']

    list_display       = (
        'title', 'created_by', 'created_on', 'published_on',
        'status', 'comment_count', 'showing', 'commenting',
        'comments_moderation',
    )
    list_display_links = ('title',)
    list_filter        = ('status', )
    list_per_page      = 50
    search_fields      = (
        'title', 'created_by__username', 'created_by__nickname', 'created_by__email',
    )
    list_select_related = True

    def save_model(self, request, post, form, change):
        if not change:
            post.created_by = get_profile(request)
        else:
            post.edited_by = get_profile(request)

        was_draft = True
        if change:
            was_draft = Post.objects.get(pk=post.pk).status == Post.statuses.draft

        if was_draft and post.is_published:
            post.publicate(form.cleaned_data['notify'])
        else:
            post.save()

        form.save_m2m()

admin.site.register(Post, PostAdmin)

class CommentAdmin(akismet.ActionModelAdmin, admin.ModelAdmin):
    list_display = (
        'created_on', 'post', 'status', 'created_by', 'headline',
        'text_filter', 'antispam'
    )
    list_per_page = 25
    list_select_related = True

    date_hierarchy = 'created_on'
    list_filter = ('status',)

    actions = ['antispam_action_spam']

    def headline(self, comment):
        return truncate_words(comment.text, 7)
    headline.short_description = 'headline'

    def save_model(self, request, comment, form, change):
        if change:
            comment.edited_by = get_profile(request)

        comment.save()

    # Antispam related callbacks

    def antispam_map_action(self, comment):
        return comment.status in\
            (Comment.statuses.published, Comment.statuses.moderation) and 'spam' or 'ham'

    def antispam_do_action(self, action, comment):
        if action == 'spam':
            comment.status = Comment.statuses.spam
        elif action == 'ham':
            comment.status = Comment.statuses.published

        comment.save()

admin.site.register(Comment, CommentAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'post_count',
    )
    list_per_page = 25

admin.site.register(Tag, TagAdmin)
