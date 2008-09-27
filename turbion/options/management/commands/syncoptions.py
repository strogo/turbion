# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.contrib.contenttypes.models import ContentType

from turbion.options.models import Option
from turbion.options.optionset import OptionSetSpot

class Command( NoArgsCommand ):
    def handle_noargs( self, **option_set ):
        for name, option_set in OptionSetSpot.sets.iteritems():
            meta = option_set._meta

            if meta.to_object and meta.model:
                ids = meta.model.objects.values_list( "id", flat = True )
                for id in ids:
                    option_set.create( pk = id )
            else:
                option_set.create()
