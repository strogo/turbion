from turbion.core.utils import spot

class FilterManager(spot.DictSpotManager):
    def load(self):
        from turbion.core.utils.loading import get_sub_modules
        get_sub_modules("turbion.core.utils.markup", "filters")

    def get(self, key):
        self.load()
        return super(FIlterManager, self).get(key)

    def all(self):
        self.load()
        return super(FilterManager, self).all()

    def add(self, obj_type):
        obj = self.create(obj_type)
        self._objects[obj.name()] = obj

class BaseFilter(object):
    def name(self):
        return self.meta.name.lower()

    def to_html(self, value):
        raise NotImplementedError

Filter = spot.create(
    base=BaseFilter,
    manager=FilterManager
)
