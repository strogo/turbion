# -*- coding: utf-8 -*-
from django.contrib import admin

from turbion.blogs.models import Blog, Post

class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", 'slug', 'name', 'created_on', "created_by")

admin.site.register(Blog, BlogAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display       = ('blog', 'title', "created_by", 'created_on', 'status', 'comment_count', 'review_count')
    list_display_links = ('title',)
    list_filter        = ('blog', "created_by", "status",)
    list_per_page      = 50
    search_fields      = ("title", "created_by__username")

admin.site.register(Post, PostAdmin)
