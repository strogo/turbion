# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.db import models

from optparse import make_option

class Command(NoArgsCommand):
    help = 'Creates the blog infrastructure'

    requires_model_validation = True

    option_list = NoArgsCommand.option_list + (
        make_option('--owner', dest='owner', default=None,
            help='Specifies the blog\'s owner username.'),
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'),
    )

    def handle_noargs(self, owner=None, **options):
        print "Performing blog setup..."

        owner = self._get_owner(owner)

        blog = self._create_blog(owner)

        print "Blog setup successful."

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

    def _create_blog(self, owner):
        pass
