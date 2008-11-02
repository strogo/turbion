# -*- coding: utf-8 -*-
from django.core.management.base import LabelCommand
from django.db import models

from optparse import make_option

from turbion.roles.models import Role, Capability

class Command(LabelCommand):
    help = 'Create a new blog instance'
    args = "blogname"

    requires_model_validation = True

    def handle_label(self, blog_name, **options):
        print "Creating new blog..."
        print "Blog name: %s" % blog_name

        slug = self._get_slug(blog_name)
        owner = self._get_owner()

        blog = self._create_blog(blog_name, slug, owner)

        print "Blog '%s' was created successful" % blog

    def _get_slug(self, name):
        from turbion.utils.text import slugify
        default_slug = slugify(name)

        slug = raw_input("Please enter blog slug(default: %s): " % default_slug)
        if slug:
            slug = slugify(slug)
        else:
            slug = default_slug

        print "Selected slug: %s" % slug

        return slug

    def _get_owner(self):
        from turbion.profiles.models import Profile

        while True:
            name = raw_input("Please enter blog owner username: ")

            try:
                profile = Profile.objects.get(username=name)
                break
            except Profile.DoesNotExist:
                print "User with name '%s' does not exist. Try again"

        print "Selected owner: %s" % profile

        return profile

    def _create_blog(self, name, slug, owner):
        from turbion.blogs.models import Blog

        return Blog.objects.create_blog(name, slug, owner)
