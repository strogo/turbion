# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007-2008 Alexander Koshelev (daevaorn@gmail.com)
from django.conf import settings

from turbion.blogs.models.post import Post

from dxapian import XapianIndexer

indexer = XapianIndexer( model = Post,
                         fields = ( "text",
                                  ),
                        attributes = { "blog" : "blog.id",
                                       "status" : "status",
                                       "title" : "title",  },
                        trigger = ( lambda post: post.is_published )
                         )
