# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.core.management.base import BaseCommand
from optparse import make_option

class Command(BaseCommand):
    help = 'Deletes visitors with expires sessions'

    requires_model_validation = True

    def handle(self, *args, **options):
        from turbion.visitors.models import Visitor
        
        visitors = Visitor.objects.all().extra( where=["ss.session_key != visitors_visitor.session_key",
                                                       "gu.visitor_id != visitors_visitor.id" ],
                                                tables=['django_session as ss','visitors_genericuser as gu'] ).distinct()

        visitors.delete()
        
        
