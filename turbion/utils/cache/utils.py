# -*- coding: utf-8 -*-
from django.utils.functional import curry
from django.core.cache import cache
from django.utils.encoding import smart_str
from django.utils.itercompat import is_iterable

def to_list(arg):
    """Converts `arg` to list"""
    if is_iterable(arg) and not isinstance(arg, dict):
        return list(arg)
    else:
        return [arg]

def make_cache_key(base, suffix_list):
    return ":".join(map(smart_str, [base] + suffix_list))

class CacheWrapper(object):
    def __init__(self, func, trigger, suffix, base_name):
        self.trigger = trigger
        self.suffix = suffix and suffix or (lambda:[])

        self.func = func
        self.base_name = base_name
        
        self.connect_invalidators()

    def __call__(self, *args, **kwargs):
        cache_key = make_cache_key(
                        self.base_name,
                        to_list(self.suffix(*args, **kwargs))    
                    )

        value = cache.get(cache_key)

        if value is None:
            value = self.func(*args, **kwargs)

            cache.set(cache_key, value)

        return value
    
    def connect_invalidators(self):
        """Connects invalidator to all needed signals"""
        defaults = {
            "suffix" : lambda *args, **kwargs: [],
            "signal": []
        }
    
        for t in to_list(self.trigger):
            trigger = defaults.copy()
            trigger.update(t)
    
            suffix_getter = trigger["suffix"]
            sender        = trigger["sender"]
    
            signals       = trigger["signal"]
    
            for signal in to_list(signals):
                def make_cache_invalidator(suffix_getter):
                    def cache_invalidator(signal, sender, *args, **kwargs):
                        cache.delete(
                                make_cache_key(
                                    self.base_name,
                                    to_list(suffix_getter(*args, **kwargs))
                                )
                        )
                    return cache_invalidator
    
                signal.connect(
                        make_cache_invalidator(suffix_getter),
                        sender=sender,
                        weak=False
                    )
    