# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.core.management.base import NoArgsCommand
from django.bin.daily_cleanup import clean_up
from optparse import make_option

class Command(NoArgsCommand):
    help = 'Deletes expires sessions'

    requires_model_validation = True

    def handle_noargs(self, **options):
        clean_up()