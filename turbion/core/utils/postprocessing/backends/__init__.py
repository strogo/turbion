# -*- coding: utf-8 -*-
from turbion.loading import get_module_attrs

INSTALLED_BACKENDS = ["markdown", "dummy", "html"]

for back in INSTALLED_BACKENDS:
    get_module_attrs("turbion.core.utils.postprocessing.backends", back)
