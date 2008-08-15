# -*- coding: utf-8 -*-
from turbion.utils.captcha import CaptchaManager
from django.http import HttpResponse

def image(request, id):
    response = HttpResponse(mimetype ='image/jpeg')
    CaptchaManager(request).render_test(response, str(id))
    
    return response