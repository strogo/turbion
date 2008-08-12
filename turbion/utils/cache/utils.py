# -*- coding: utf-8 -*-
#--------------------------------
#$Date: 2008-08-06 23:53:57 +0400 (Wed, 06 Aug 2008) $
#$Author: daev $
#$Revision: 1792 $
#--------------------------------
#Copyright (C) 2007-2008 Alexander Koshelev (daevaorn@gmail.com)
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

def connect_invalidator(triggers, cache_key, cache_key_suffix):
    """Connects invalidator to all needed signals"""
    defaults = {"suffix" : lambda *args, **kwargs: [],
                "checker": None,
                "signal": []
            }

    for t in to_list(triggers):
        trigger = defaults.copy()
        trigger.update(t)

        suffix_getter = trigger["suffix"]
        checker       = trigger["checker"]
        sender        = trigger["sender"]

        signals       = trigger["signal"]

        for signal in to_list(signals):
            def make_cache_invalidator(suffix_getter):
                def cache_invalidator(signal, sender, *args, **kwargs):
                    if checker is not None:
                        if checker(*args, **kwargs):
                            cache.delete(cache_key)
                        else:
                            return
                    else:
                        if cache_key_suffix == to_list(suffix_getter(*args, **kwargs)):
                            cache.delete(cache_key)
                return cache_invalidator

            signal.connect(make_cache_invalidator(suffix_getter),
                            sender=sender,
                            weak=False,
                            dispatch_uid=cache_key
                        )

class CacheWrapper(object):
    def __init__(self, func, trigger, suffix, base_name):
        self.trigger = trigger
        self.suffix = suffix and suffix or (lambda:[])

        self.func = func
        self.base_name = base_name

    def __call__(self, *args, **kwargs):
        cache_key_suffix = to_list(self.suffix(*args, **kwargs))
        cache_key = make_cache_key(self.base_name, cache_key_suffix)

        value = cache.get(cache_key)

        connect_invalidator(self.trigger, cache_key, cache_key_suffix)

        if value is None:
            value = self.func(*args, **kwargs)

            cache.set(cache_key, value)

        return value
