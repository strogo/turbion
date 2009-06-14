from turbion.core.utils import spot

class FilterManager(spot.SpotManager):
    def load(self):
        from turbion.core.utils.loading import get_sub_modules
        get_sub_modules("turbion.core.utils.markup", "filters")

class BaseFilter(object):
    def is_safe(self):
        return True

    def to_html(self, value):
        raise NotImplementedError

Filter = spot.create(BaseFilter, manager=FilterManager)
