# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.core.urlresolvers import reverse
from django import newforms as forms

from turbion.blogs.decorators import blog_view, titled
from turbion.blogs.models import Post
from turbion.blogs.models import Comment
from turbion.tags.models import Tag

from pantheon.utils.decorators import templated, paged

class SearchForm( forms.Form ):
    query = forms.CharField( required = True, label = 'Поиск' )

def generic_search( request, models, filters = {}, form_name = "form" ):
    context = {}

    if request.GET:
        form = SearchForm( request.GET )
        if form.is_valid():
            query = form.cleaned_data[ "query" ]
            context[ "query" ] = query

            for model in models:
                new_query = query
                model_name = model.__name__.lower()
                filter = filters.get( model_name, {} )
                append_query = u" AND ".join( [ "%s:%s" % pair for pair in filter.iteritems() ] )
                if append_query:
                    new_query += " AND " + append_query

                resultset = model.indexer.search( query = new_query )

                context[ "%s_results" % model_name ] = resultset
    else:
        form = SearchForm()

    context[ form_name ] = form

    return context

def filter_ids( resultset, ids ):
    return [ res for res in resultset if res.get_pk() in ids ]

def get_ids( queryset ):
    return [ d["id"] for d in queryset.values( "id" ) ]

@paged
@blog_view
@templated( 'turbion/blogs/search/results.html' )
@titled( page = u'Поиск' )
def search( request, blog ):
    blog_search_action = reverse( "turbion.blogs.views.search.search",
                                  kwargs = { "blog" : blog.slug } )

    context = { "blog" : blog,
                "blog_search_action" : blog_search_action,
            }

    context.update( generic_search( request,
                                    models = [ Post, Comment ],
                                    filters = { "post" : { "blog" : blog.id, "status" : Post.statuses.published } },
                                   )
                     )

    if "comment_results" in context:
        context[ "comment_results" ] = filter_ids( context[ "comment_results" ],
                                               get_ids( Comment.published.for_object( blog ) )
                                             )
    return context

@paged
@blog_view
@templated( 'turbion/blogs/search/posts.html' )
@titled( page = u'Поиск в постах' )
def posts( request, blog ):
    blog_search_action = reverse( "turbion.blogs.views.search.posts",
                                  kwargs = { "blog" : blog.slug } )
    context = { "blog" : blog, "blog_search_action" : blog_search_action }

    context.update( generic_search( request,
                                    models = ( Post, ),
                                    filters = { "post" : { "blog" : blog.id, "status" : Post.statuses.published } },
                                    ) )
    return context

@paged
@blog_view
@templated( 'turbion/blogs/search/comments.html' )
@titled( page = u'Поиск в комментариях' )
def comments( request, blog ):
    blog_search_action = reverse( "turbion.blogs.views.search.comments",
                                  kwargs = { "blog" : blog.author.username } )
    context = { "blog" : blog, "blog_search_action" : blog_search_action }

    context.update( generic_search( request,
                                    models = ( Comment, ),
                                    ) )
    context[ "comment_results" ]=  filter_ids( context[ "comment_results" ],
                                               get_ids( Comment.published.for_object( blog ) )
                                             )

    return context
