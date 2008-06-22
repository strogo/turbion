# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from datetime import datetime

class VisitorsMiddleware(object):
    def process_request( self, request ):
        if request.generic_user:
            request.generic_user.last_visit = datetime.now()
            request.generic_user.save()
