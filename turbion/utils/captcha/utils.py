# -*- coding: utf-8 -*-
from turbion.utils.captcha import CaptchaManager

def get_solution(form, field_name="captcha"):
    captcha_field = form[field_name]
    
    request = captcha_field.request
    id = captcah_field.get_id()
    
    manager = CaptchaManager(self.request)
    test = manager.get_test(id)
    
    return test.solutions[0]