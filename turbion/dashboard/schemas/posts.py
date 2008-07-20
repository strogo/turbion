# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2008 Alexander Koshelev (daevaorn@gmail.com)
from turbion.dashboard.schemas import Schema

from turbion.blogs.models import Post

class PostsSchame(Schema):
    name = "posts"
    model = Post
    fields = ['id','created_on','title']

    def get_query_set(self):
        return Post.objects.for_blog(self.blog)
