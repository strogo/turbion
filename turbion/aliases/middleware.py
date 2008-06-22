# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django import http

from turbion.aliases.models import Alias

import re

FEEDBURNER_REG = re.compile( '(feedburner|feedvalidator)', re.I )

class AliasesMiddleware( object ):
    def process_request(self, request):
        try:
            alias = Alias.active.get( from_url = request.path )
            if not FEEDBURNER_REG.match( request.META.get( "HTTP_USER_AGENT", "" ) ):
                return http.HttpResponseRedirect( alias.to_url )
        except Alias.DoesNotExist:
            pass
