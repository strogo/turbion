from turbion.bits.cache.utils import CacheWrapper

def cached(trigger, suffix=None, base_name=None):
    def _wrapper(func):
        if base_name == None:
            real_base_name = func.__module__ + "." + func.__name__
        else:
            real_base_name = base_name

        return CacheWrapper(func, trigger, suffix, real_base_name)
    return _wrapper
