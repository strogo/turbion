
class Spot(object):
    pass

class SpotManager(object):
    def __init__(self):
        self._objects = []

    def all(self):
        return self._objects

    def create(self, obj_type):
        return obj_type()

    def add(self, obj_type):
        self._objects.append(self.create(obj_type))

class DictSpotManager(SpotManager):
    def __init__(self):
        self._objects = {}

    def all(self):
        return self._objects.items()

    def get(self, key):
        return self._objects[key]

    def add(self, obj_type):
        self._objects[obj_type.meta.descriptor] = self.create(obj_type)

class SpotMeta(object):
    def __init__(self, name, descriptor):
        self.name = name
        self.descriptor = descriptor

def create(base=Spot, manager=SpotManager, meta=SpotMeta):
    class _SpotMetaclass(type):
        def __new__(cls, name, bases, attrs):
            try:
                _Spot
            except NameError:
                cls.manager = manager()
                t = super(_SpotMetaclass, cls).__new__(cls, name, bases, attrs)
            else:
                t = super(_SpotMetaclass, cls).__new__(cls, name, bases, attrs)

                t.meta = meta(name, "%s.%s" % (t.__module__, name))

                cls.manager.add(t)

            return t

    class _Spot(base):
        __metaclass__ = _SpotMetaclass

    return _Spot
