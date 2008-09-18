# -*- coding: utf-8 -*-
from django.test import TestCase
from django import forms

from turbion.utils.testing import create_request
from turbion.utils.captcha.forms import CaptchaField


class CaptchaImageTest(TestCase):
    def setUp(self):
        pass
    
    def test_image_generation(self):
        pass

class CaptchaFormTest(TestCase):
    def setUp(self):
        request = create_request()
        
        class TestForm(forms.Form):
            captcha = CaptchaField(request=request)
            
        self.form_class = TestForm
        
        TestForm().as_p()
    
    def test_form_rendering(self):
        pass
    
    def test_form_validation(self):
        solution = get_solution(self.form_class)
        data = {"captcha": solution}
        
        form = self.form_class(data=data)
        
        self.assert_(form.is_valid())
        
        illegal_data = {"captcha": "*%s*" % solution}
        
        form = self.form_class(data=illegal_data)
        
        self.assert_(not form.is_valid())
    
    def test_form_error_report(self):
        pass
    
class CaptchaInvalidationTest(TestCase):
    pass