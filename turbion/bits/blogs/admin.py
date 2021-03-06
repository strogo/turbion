from django import forms
from django.utils.text import truncate_words
from django.utils.encoding import force_unicode
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from turbion.bits.blogs.models import Post, Comment, Tag
from turbion.bits.profiles import get_profile
from turbion.bits.antispam.admin import ActionModelAdmin

class PostAdmin(admin.ModelAdmin):
    exclude = ['created_by', 'edited_by']

    list_display       = (
        'title', 'created_by', 'created_on', 'published_on',
        'status', 'comment_count', 'showing', 'commenting',
        'comments_moderation'
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
            post.publicate()
        else:
            post.save()

        form.save_m2m()

admin.site.register(Post, PostAdmin)

class CommentAdmin(ActionModelAdmin, admin.ModelAdmin):
    list_display = [
        'created_on', 'post', '_status', 'created_by', 'headline',
        'text_filter'
    ] + ActionModelAdmin.additinal_fields

    list_per_page = 25
    list_select_related = True

    date_hierarchy = 'created_on'
    list_filter = ('status',)

    actions = ActionModelAdmin.batch_actions

    def _status(self, comment):
        if comment.status == Comment.statuses.spam:
            return '%s: %s' % (comment.get_status_display(), comment.antispam_status)
        return comment.get_status_display()
    _status.short_description = _('status')

    def headline(self, comment):
        return truncate_words(comment.text, 10)
    headline.short_description = _('headline')

    def save_model(self, request, comment, form, change):
        if change:
            comment.edited_by = get_profile(request)

        comment.save()

admin.site.register(Comment, CommentAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'post_count',
    )
    list_per_page = 25

admin.site.register(Tag, TagAdmin)
