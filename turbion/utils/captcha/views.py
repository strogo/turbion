# -*- coding: utf-8 -*-
from turbion.utils.captcha import CaptchaManager
from django.http import HttpResponse

def image(request, id):
    print request.session.items()
    response = HttpResponse(mimetype ='image/jpeg')
    CaptchaManager(request.session).render_test(response, str(id))

    return response
