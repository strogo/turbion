# -*- coding: utf-8 -*-
from turbion.utils.captcha import CaptchaManager

def get_solution(request, id=None):
    manager = CaptchaManager(request.session)
    if id:
        test = manager.get_test(id)
    else:
        test = manager.factory.storedInstances.values()[0]

    return test.solutions[0]
