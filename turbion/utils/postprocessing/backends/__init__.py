# -*- coding: utf-8 -*-
INSTALLED_BACKENDS = [ "markdown", "dummy", "html" ]

for back in INSTALLED_BACKENDS:
    name = "turbion.utils.postprocessing.backends.%s" % back
    mod = __import__( name, {}, {}, [ "" ] )
