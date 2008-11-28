# -*- coding: utf-8 -*-
from turbion import admin
from turbion.blogs.models import Blog, Post

class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", 'slug', 'name', 'created_on', "created_by")

admin.site.register(Blog, BlogAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display       = (
        'blog', 'title', "created_by", 'created_on', 'published_on',
        'status', 'comment_count'
    )
    list_display_links = ('title',)
    list_filter        = ('blog', "status", "created_by",)
    list_per_page      = 50
    search_fields      = (
        "title", "created_by__username", "created_by__nickname",
        "created_by__email",
    )

admin.site.register(Post, PostAdmin)
