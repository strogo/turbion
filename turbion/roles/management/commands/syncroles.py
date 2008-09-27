# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.db import models
from django.contrib.contenttypes.models import ContentType

from optparse import make_option

from turbion.roles.models import Role, Capability

class Command(NoArgsCommand):
    help = 'Sync roles and its capabilities.'

    requires_model_validation = True

    def handle_noargs(self, **options):
        for role in Role.objects.all():
            pass
