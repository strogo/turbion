# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.core.management.base import NoArgsCommand
from optparse import make_option

class Command(BaseCommand):
    help = 'Deletes visitors with expires sessions'

    requires_model_validation = True

    def handle_noargs(self, **options):
        from turbion.visitors.models import Visitor, User
        from django.contrib.contenttypes.models import ContentType

        visitors = Visitor.objects.all().extra( where=["ss.session_key != visitors_visitor.session_key",
                                                       "gu.visitor_id != visitors_visitor.id" ],
                                                tables=['django_session as ss','visitors_genericuser as gu'] ).distinct()

        visitors.delete()
