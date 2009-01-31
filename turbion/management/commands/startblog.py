# -*- coding: utf-8 -*-
from django.core.management.base import LabelCommand
from django.db import models

from optparse import make_option

from turbion.core.roles.models import Role, Capability

class Command(LabelCommand):
    help = 'Create a new blog instance'
    args = "blogname"

    requires_model_validation = True

    option_list = LabelCommand.option_list + (
        make_option('--slug', dest='slug', default=None,
            help='Specifies the slug for the blog.'),
        make_option('--owner', dest='owner', default=None,
            help='Specifies the blog\'s owner username.'),
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'),
    )

    def handle_label(self, blog_name, slug=None, owner=None, **options):
        print "Creating new blog..."
        print "Blog name: %s" % blog_name

        if not slug:
            slug = self._get_slug(blog_name)

        owner = self._get_owner(owner)

        blog = self._create_blog(blog_name, slug, owner)

        print "Blog '%s' created successful." % blog

    def _get_slug(self, name):
        from turbion.core.utils.text import slugify
        default_slug = slugify(name)

        slug = raw_input("Please enter blog slug(default: %s): " % default_slug)
        if slug:
            slug = slugify(slug)
        else:
            slug = default_slug

        print "Selected slug: %s" % slug

        return slug

    def _get_owner(self, name=None):
        from turbion.core.profiles.models import Profile

        while True:
            if not name:
                name = raw_input("Please enter blog owner username: ")

            try:
                profile = Profile.objects.get(username=name)
                break
            except Profile.DoesNotExist:
                print "User with name '%s' does not exist. Try again" % name
                name = None

        print "Selected owner: %s" % profile

        return profile

    def _create_blog(self, name, slug, owner):
        from turbion.core.blogs.models import Blog

        return Blog.objects.create_blog(name, slug, owner)
