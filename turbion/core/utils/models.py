import operator

from django.db import models

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

def add_q_prefix(q, prefix):
    """
        Adds speciffic prefix to lookup fields
    """
    new_q = models.Q()
    new_q.connector = q.connector
    new_q.negated = q.negated

    for child in q.children:
        if isinstance(child, models.Q):
            new_q.children.append(
                add_q_prefix(child, prefix)
            )
        else:
            new_q.children.append((
                prefix + child[0],
                child[1]
            ))

    return new_q

class FilteredManager(models.Manager):
    """
        Generic simple filtered manager
    """
    def __init__(self, *args_lookups, **kwargs_lookups):
        self.args_lookups = args_lookups
        self.kwargs_lookups = kwargs_lookups

        super(FilteredManager, self).__init__()

    def get_query_set(self):
        return self.apply_lookup(super(FilteredManager, self).get_query_set())

    def get_lookup(self, prefix=None):
        if not prefix:
            args_lookups = self.args_lookups
            kwargs_lookups = self.kwargs_lookups
        else:
            args_lookups = [add_q_prefix(q, prefix) for q in self.args_lookups]
            kwargs_lookups = dict(
                [(prefix + field, value) for field, value in self.kwargs_lookups.iteritems()]
            )

        if not args_lookups:
            args_lookups = [models.Q()]

        return reduce(
            operator.and_,
            list(args_lookups) + [
                models.Q(**{key: value}) for key, value in kwargs_lookups.iteritems()
            ]
        )

    def apply_lookup(self, qs, prefix=None):
        return qs.filter(
            self.get_lookup(prefix)
        )
