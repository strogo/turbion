from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from turbion.core.blogs.decorators import titled
from turbion.core.blogs.models import Post, Comment
from turbion.core.blogs.forms import SearchForm
from turbion.core.utils.pagination import paginate
from turbion.core.utils.decorators import templated, paged

def generic_search(request, models, filters={}, form_name="form", page=1):
    context = {}

    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            context["query"] = query

            for model in models:
                new_query = query
                model_name = model.__name__.lower()
                filter = filters.get(model_name, {})

                resultset = model.indexer.search(query=query).prefetch()

                result_page = paginate(
                    resultset,
                    page,
                    settings.TURBION_BLOG_POSTS_PER_PAGE
                )

                context["%s_page" % model_name] = result_page
    else:
        form = SearchForm()

    context[form_name] = form

    return context

@paged
@templated('turbion/blogs/search_results.html')
@titled(page=_('Search'))
def search(request):
    blog_search_action = reverse("turbion_blog_search")

    context = {
        "blog_search_action": blog_search_action,
    }

    context.update(
        generic_search(
            request,
            models=[Post, Comment],
            filters={"post": {"status": Post.statuses.published}},
            page=request.page,
        )
    )

    return context

@paged
@templated('turbion/blogs/search_results.html')
@titled(page=_('Search in posts'))
def posts(request):
    blog_search_action = reverse("turbion_blog_search_posts")

    context = {
        "blog_search_action": blog_search_action
    }

    context.update(
        generic_search(
            request,
            models=(Post,),
            filters={"post": {"status": Post.statuses.published}},
        )
    )
    return context

@paged
@templated('turbion/blogs/search_results.html')
@titled(page=_('Search in comments'))
def comments(request):
    blog_search_action = reverse("turbion_blog_search_comments")

    context = {
        "blog_search_action": blog_search_action
    }

    context.update(
        generic_search(
            request,
            models=(Comment,),
        )
    )

    return context
