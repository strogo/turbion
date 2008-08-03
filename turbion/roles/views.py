# -*- coding: utf-8 -*-
from pantheon.utils.decorators import titled, templated

@templated( "turbion/roles/no_capability.html" )
@titled(  )
def no_capability( request ):
    return {}
