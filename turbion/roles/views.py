# -*- coding: utf-8 -*-
from turbion.utils.decorators import titled, templated

@templated( "turbion/roles/no_capability.html" )
@titled(  )
def no_capability( request ):
    return {}
