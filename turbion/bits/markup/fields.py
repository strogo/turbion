from django.db import models
from django.utils.translation import ugettext_lazy as _

from turbion.bits.markup.filters import Filter

class MarkupField(models.CharField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, safe=True, limit_choices_to=None, *args, **kwargs):
        self.limit_choices_to = limit_choices_to
        self.safe = safe

        def _check(name, filter):
            if limit_choices_to and name not in limit_choices_to:
                return False

            if safe and not filter.is_safe():
                return False

            return True

        defaults = {
            "choices": [(name, name) for name, filter in Filter.manager.all()\
                                    if _check(name, filter)],
            "max_length": 50,
            "default": "markdown"
        }

        defaults.update(kwargs)

        super(MarkupField, self).__init__(*args, **defaults)

class MarkupTextField(models.TextField):
    def __init__(self, *args, **kwargs):
        self.processing = kwargs.pop("processing", False)
        self.html_name = kwargs.pop("html_name", None)
        self.filter_field_name = kwargs.pop("filter_field_name", None)
        self.limit_choices_to = kwargs.pop("limit_choices_to", None)
        self.safe = kwargs.pop('safe', True)

        super(MarkupTextField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        super(MarkupTextField, self).contribute_to_class(cls, name)

        if self.html_name is None:
            self.html_name = "%s_html" % name

        if self.filter_field_name is None:
            self.filter_field_name = "%s_filter" % name

        models.TextField(
            editable=False, blank=True
        ).contribute_to_class(cls, self.html_name)
        MarkupField(
            verbose_name=_("markup filter"),
            limit_choices_to=self.limit_choices_to,
            safe=self.safe
        ).contribute_to_class(cls, self.filter_field_name)

    def pre_save(self, model_instance, add):
        value = super(MarkupTextField, self).pre_save(model_instance, add)

        if self.processing:
            from turbion.bits.markup import processing
            value = processing.render_string(value)

        filter = getattr(model_instance, self.filter_field_name)

        setattr(
            model_instance,
            self.html_name,
            Filter.manager.get(filter).to_html(value)
        )

        return value
