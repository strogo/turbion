# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from pantheon.utils.decorators import titled, templated

@templated( "roles/no_capability.html" )
@titled(  )
def no_capability( request ):
    return {}
