# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2008 Alexander Koshelev (daevaorn@gmail.com)
from datetime import datetime

from django.core.management.base import NoArgsCommand
from optparse import make_option

from django.contrib.sessions.models import Session
from turbion.visitors.models import Visitor, User

class Command(NoArgsCommand):
    help = 'Deletes visitors with expires session and users with no references'

    option_list = NoArgsCommand.option_list + (
        make_option('--dry', action='store_true', dest='dry',
            help='Do not perform real delete.'),
    )

    requires_model_validation = True

    def handle_noargs(self, **options):
        self.dry = options.get("dry")

        self._cleanup_visitors()
        self._cleanup_users()

    def _cleanup_visitors(self):
        related_fields = Visitor._meta.get_all_related_objects()

        total_count = Visitor.objects.all().count()
        deleted_count = 0

        for visitor in Visitor.objects.all():
            try:
                Session.objects.get(session_key=visitor.session_key, expire_date__gte=datetime.now())
            except Session.DoesNotExist:
                if not visitor.user.count() and not self._has_references(visitor, related_fields):
                    deleted_count += 1
                    if not self.dry:
                        visitor.delete()

        print "Deleted %s from %s visitors" % (deleted_count, total_count)

    def _cleanup_users(self):
        related_fields = User._meta.get_all_related_objects()

        total_count = User.objects.all().count()
        deleted_count = 0

        for user in User.guests.all():
            #check whenever have links to this user
            if self._has_references(user, related_fields):
                continue

            #check visitor session expires
            visitor = user.raw_user

            try:
                Session.objects.get(session_key=visitor.session_key, expire_date__gte=datetime.now())
            except Session.DoesNotExist:
                deleted_count += 1
                if not self.dry:
                    user.delete()

        print "Deleted %s from %s users" % (deleted_count, total_count)

    def _has_references(self, instance, fields):
        has_reference = False
        for field in fields:
            model = field.model

            objs = model._default_manager.filter(**{field.field.name: instance})

            has_reference = objs.count() > 0

        return has_reference
