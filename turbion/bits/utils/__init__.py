
def memoize(func):
    def _decorator(self, *args, **kwargs):
        attr_name = "_%s" % func.__name__

        if not hasattr(self, attr_name):
            res = func(self, *args, **kwargs)
            setattr(self, attr_name, res)
        return getattr(self, attr_name)
    _decorator.__doc__ = func.__doc__
    _decorator.__dict__ = func.__dict__
    return _decorator
