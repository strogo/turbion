# -*- coding: utf-8 -*-
from Captcha.Visual import Tests
import Captcha
import time

from django.conf import settings
from django.http import Http404

from django.utils.encoding import smart_str

class SessionStore(object):
    def __init__(self, session):
        """
        data = {key: (test, data)}
        """
        self.session = session

        self._data = session.setdefault("turbion_captcha", {})

    def __getitem__(self, key):
        return self._data[key][0]

    def __setitem__(self, key, value):
        self._data[key] = (value, time.time())

    def __delitem__(self, key):
        try:
            del self._data[key]
        except KeyError:
            pass

    def keys(self):
        return self._data.keys()

    def values(self):
        return [i[1][0] for i in self._data.items()]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def sync(self):
        pass

    def __iter__(self):
        return self._data.iteritems()

    def __len__(self):
        return len(self._data)

class SessionFactory(Captcha.Factory):
    def __init__(self, request, lifetime=60*15):
        Captcha.Factory.__init__(self, lifetime)
        self.storedInstances = SessionStore(request)

    def clean(self):
        """Removed expired tests"""
        border = time.time() - self.lifetime

        for key, value in self.storedInstances._data.items():
            if value[1] < border:
                del self.storedInstances[key]

class CaptchaManager(object):
    def __init__(self, session):
        self.factory = SessionFactory(session)
        session["__turbion_captcha_access"] = time.time()

    def make_test(self):
        test_class = Tests.PseudoGimpy
        test = self.factory.new(test_class)
        self.factory.clean()

        return test

    def get_test(self, id):
        test = self.factory.get(id)
        return test

    def render_test(self, response, id, type='JPEG'):
        test = self.get_test(id)

        if test is not None:
            test.render().save(response, type)
        else:
            raise Http404

    def get_solution(self, id, pos=0):
        test = self.get_test(id)
        return test.solutions[pos]
