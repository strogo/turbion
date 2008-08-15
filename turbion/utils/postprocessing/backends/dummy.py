# -*- coding: utf-8 -*-
from turbion.utils.postprocessing.backends.base import BaseProcessor

class Processor(BaseProcessor):
    name = "dummy"

    def preprocess(self, value ):
        return value

    def postprocess( self, value ):
        return value
