# -*- coding: utf-8 -*-
from django import http
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from turbion.utils.decorators import templated
from turbion.dashboard.decorators import titled

from turbion.blogs.models.blog import Blog, BlogRoles
from turbion.dashboard import forms, decorators
from turbion.profiles.models import Profile


@templated("turbion/dashboard/global/install.html")
@titled(page=_("Instalation"))
def install(request):
    if not Profile.objects.has_superuser():
        return http.HttpResponseRedirect(reverse("dashboard_create_superuser"))

    return {}

@login_required
@decorators.superuser_required
@templated("turbion/dashboard/global/index.html")
@titled(page=_("Index"))
def index(request):
    blogs = Blog.objects.all()

    if not len(blogs):
        return http.HttpResponseRedirect(reverse("dashboard_create_blog"))

    return {"blogs": blogs}


@templated( "turbion/dashboard/global/create_superuser.html" )
@titled(page=_("Superuser creation"))
def create_superuser( request ):
    if Profile.objects.has_superuser():
        return http.HttpResponseRedirect( reverse( "dashboard_index" ) )

    if request.POST:
        form = forms.CreateSuperuserForm( request.POST )
        if form.is_valid():
            user = form.save()

            return http.HttpResponseRedirect( reverse( "dashboard_create_blog" ) )
    else:
        form = forms.CreateSuperuserForm()

    return { "form" : form }

@login_required
@decorators.superuser_required
@templated("turbion/dashboard/global/create_blog.html")
@titled(page=_("New blog creation"))
def create_blog(request):
    if request.POST:
        form = forms.CreateBlogForm(request.POST)
        if form.is_valid():
            blog = form.save(False)
            blog.created_by = request.user
            blog.save()

            owner = form.cleaned_data["owner"]

            BlogRoles.roles.blog_owner.grant(owner, blog)

            return http.HttpResponseRedirect(blog.get_dashboard_url())
    else:
        form = forms.CreateBlogForm()

    return {"form": form}

@templated('turbion/dashboard/global/login.html')
@titled(page=_("Login"))
def login(request):
    if request.POST:
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            auth.login(request, user)

            return http.HttpResponseRedirect(request.GET.get('next', user.get_absolute_url()))
    else:
        form = forms.LoginForm()

    return {
        "form": form
    }

@login_required
@templated('turbion/dashboard/global/logout.html')
@titled(page=_("Logout"))
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return  http.HttpResponseRedirect(request.GET.get('next', '/'))
