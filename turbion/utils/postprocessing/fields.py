# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from turbion.utils.postprocessing import ProcessorSpot, postprocess

class PostprocessField(models.CharField):
    __metaclass__ = models.SubfieldBase

    default_choices = [(name, name) for name in ProcessorSpot.processors.keys()]

    def __init__(self, limit_choices_to=None, *args, **kwargs):
        self.limit_choices_to = limit_choices_to

        defaults = {
            "choices": [(label, name) for label, name in self.default_choices\
                            if limit_choices_to and name in limit_choices_to or True],
            "max_length": 50,
            "default": "dummy"
        }

        defaults.update(kwargs)

        super(PostprocessField, self).__init__(*args, **defaults)

class PostprocessedTextField(models.TextField):
    def __init__(self, *args, **kwargs):
        self.html_name = kwargs.pop("html_name", None)
        self.postprocessor_name = kwargs.pop("postprocessor_name", None)

        super(PostprocessedTextField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        super(PostprocessedTextField, self).contribute_to_class(cls, name)

        if self.html_name is None:
            self.html_name = "%s_html" % name

        if self.postprocessor_name is None:
            self.postprocessor_name = "%s_postprocessor" % name

        models.TextField(editable=False, blank=True).contribute_to_class(cls, self.html_name)
        PostprocessField(verbose_name=_("postprocessor")).contribute_to_class(cls, self.postprocessor_name)

    def pre_save(self, model_instance, add):
        value = super(PostprocessedTextField, self).pre_save(model_instance, add)

        processor = getattr(model_instance, self.postprocessor_name)

        setattr(model_instance, self.html_name, postprocess(value, processor))

        return value
