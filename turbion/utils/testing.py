# -*- coding: utf-8 -*-
from django.test import TestCase
from django import http

class BaseViewTest(TestCase):
    def assertStatus(self, url, status=http.HttpResponse.status_code, data={}):
        response = self.client.get(url, data=data)

        self.assertEqual(response.status_code, status)

        return response
    
    def hack_captcha(self, response):
        #HASH_RE = re.compile( "name=\"captcha_0\" value=\"(\w+)\"" )

        #m = HASH_RE.search(response.content)
        #if m:
        #    hash = m.groups()[0]
        #
        #    test = manager.factory.get(hash)
        #    captcha = test.solutions[0]
        #else:
        #    captcha = ""
        #    hash = ""
        
        return {
            #"captcha_0" : hash,
            #"captcha_2" : captcha
        }
