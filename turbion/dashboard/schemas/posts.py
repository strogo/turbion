# -*- coding: utf-8 -*-
from turbion.dashboard.schemas import Schema

from turbion.blogs.models import Post

class PostsSchema(Schema):
    name = "posts"
    model = Post
    fields = ['id', 'created_on', 'title', 'status', 'get_absolute_url']

    def get_query_set(self):
        return Post.objects.for_blog(self.blog)
