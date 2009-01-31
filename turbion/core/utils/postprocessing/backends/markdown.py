# -*- coding: utf-8 -*-
from turbion.core.utils.postprocessing.backends.base import BaseProcessor

class Processor(BaseProcessor):
    name = "markdown"

    def preprocess(self, value):
        return value

    def postprocess(self, value):
        import markdown2
        return markdown2.markdown( value, extras=set(["code-color"]))
