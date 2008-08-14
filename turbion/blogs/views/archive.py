# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from pantheon.utils.decorators import paged, templated
from turbion.utils.pagination import paginate

from turbion.blogs.decorators import blog_view, titled
from turbion.blogs.models import Post

from datetime import date

@blog_view
@paged
@templated( 'turbion/blogs/list.html' )
@titled( page = u'Архив блог от {{blog.calendar.current.year}}' )
def year( request, blog, year_id ):
    blog.calendar.current = date( year = int( year_id ), month = 1, day = 1 )
    post_paginator = paginate( Post.published.for_blog( blog ).filter( created_on__year = year_id ),
                               request.page,
                               blog.post_per_page )

    return { "post_paginator" : post_paginator, "blog" : blog }

@blog_view
@paged
@templated( 'turbion/blogs/list.html' )
@titled( page = u'Архив от {{blog.calendar.current.year}}/{{blog.calendar.current.month}}' )
def month( request, blog, year_id, month_id ):
    blog.calendar.current = date( year = int( year_id ), month = int( month_id ), day = 1 )
    post_paginator = paginate( Post.published.for_blog( blog ).filter( created_on__year = int(year_id),
                                                                       created_on__month = int(month_id)  ),
                               request.page,
                               blog.post_per_page )

    return { "post_paginator" : post_paginator,
            "blog" : blog,
             }

@blog_view
@paged
@templated( 'turbion/blogs/list.html' )
@titled( page = u'Архив от {{blog.calendar.current.year}}/{{blog.calendar.current.month}}/{{blog.calendar.current.day}}' )
def day( request, blog, year_id, month_id, day_id ):
    blog.calendar.current = date( year = int( year_id ), month = int( month_id ), day = int( day_id ) )
    post_paginator = paginate( Post.published.for_blog( blog ).filter( created_on__year = year_id,
                                                                       created_on__month = month_id,
                                                                       created_on__day = day_id ),
                              request.page,
                              blog.post_per_page )

    return { "post_paginator" : post_paginator,
            "blog" : blog,
            }
