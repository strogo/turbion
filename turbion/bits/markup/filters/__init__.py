from turbion.bits.utils import spot

class FilterManager(spot.Manager):
    def load(self):
        from turbion.bits.utils.loading import get_sub_modules
        get_sub_modules("turbion.bits.markup", "filters")

class BaseFilter(object):
    def is_safe(self):
        return True

    def to_html(self, value):
        raise NotImplementedError

Filter = spot.create(BaseFilter, manager=FilterManager)
