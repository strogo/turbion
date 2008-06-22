# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.core.management.base import NoArgsCommand

from turbion.gears.gear import GearSpot

class Command(NoArgsCommand):
    help = 'Revolve (executes) all needed gears once'

    requires_model_validation = True

    def handle_noargs(self, **options):
        GearSpot.revolve_all()
