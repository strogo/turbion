# -*- coding: utf-8 -*-
from turbion.core.utils.postprocessing.backends.base import BaseProcessor

class Processor(BaseProcessor):
    name = "html"
    
    def preprocess( self, value ):
        from turbion.core.utils.postprocessing.templatetags.postprocess import sanitize
        return sanitize( value )

    def postprocess( self, value ):
        return value
