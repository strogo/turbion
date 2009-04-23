from django.db import models

class GenericManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super(GenericManager, self).__init__()
        self.args = args
        self.lookups = self.selectors = kwargs

    def get_query_set(self):
        return super(GenericManager, self).get_query_set().filter(*self.args, **self.selectors)

class SlugField(models.SlugField):
    def __init__(self, prepopulate_from, *args, **kwargs):
        self.prepopulate_from = prepopulate_from
        super(SlugField, self).__init__(*args, **kwargs)

    def _get_val_from_obj(self, obj):
        from turbion.core.utils.text import slugify

        if obj:
            val = getattr(obj, self.attname, None)
            if not val:
                val = slugify("".join([getattr(obj, name) for name in self.prepopulate_from if hasattr(obj, name)]))
            return val
        return self.get_default()
