import re

SPLIT_RE = re.compile('([A-Z][a-z]*)')

class SpotManager(object):
    def __init__(self, cache=True):
        self._classes = {}
        self._objects = {}
        self._cache = cache
        self._loaded = not hasattr(self, 'load')

    def create(self, obj_class):
        if not self._cache:
            return obj_class()
        else:
            if obj_class not in self._objects:
                self._objects[obj_class] = obj_class()
            return self._objects[obj_class]

    def all_names(self):
        return self._classes.keys()

    def all(self):
        self._load()
        return [
            (name, self.create(obj_class)) for name, obj_class in self._classes.iteritems()
        ]

    def get(self, name):
        self._load()
        return self.create(self._classes[name])

    def add(self, name, obj_class):
        self._classes[name] = obj_class

    def is_loaded(self):
        return self._loaded

    def _load(self):
        if not self._loaded:
            self.load()
            self._loaded = True

def create(base, manager=SpotManager, cache=True):
    class SpotMetaclass(type):
        def __new__(cls, name, bases, attrs):
            try:
                Spot
            except NameError:
                cls.manager = manager(cache)
                t = super(SpotMetaclass, cls).__new__(cls, name, bases, attrs)
            else:
                t = super(SpotMetaclass, cls).__new__(cls, name, bases, attrs)

                if 'name' in attrs:
                    descriptor = attrs['name']
                else:
                    descriptor = '_'.join(
                        [bit.lower() for bit in SPLIT_RE.split(name) if bit]
                    )
                    attrs['name'] = descriptor

                cls.manager.add(descriptor, t)

            return t

    class Spot(base):
        __metaclass__ = SpotMetaclass

    return Spot
