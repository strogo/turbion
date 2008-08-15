# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007-2008 Alexander Koshelev (daevaorn@gmail.com)
INSTALLED_BACKENDS = [ "markdown", "dummy", "html" ]

for back in INSTALLED_BACKENDS:
    name = "turbion.utils.postprocessing.backends.%s" % back
    mod = __import__( name, {}, {}, [ "" ] )
