# -*- coding: utf-8 -*-
from django.test import TestCase
from django import forms

from turbion.utils.testing import RequestFactory
from turbion.utils.captcha.forms import CaptchaField
from turbion.utils.captcha.utils import get_solution

class CaptchaImageTest(TestCase):
    def setUp(self):
        pass

    def test_image_generation(self):
        pass

class CaptchaFormTest(TestCase):
    def setUp(self):
        request = RequestFactory().get("/")

        class TestForm(forms.Form):
            captcha = CaptchaField(request=request)

        self.form_class = TestForm

        TestForm().as_p()
        self.request = request

    def test_form_rendering(self):
        pass

    def test_form_validation(self):
        solution = get_solution(self.request)

        solution = self.request.session["turbion_captcha"].values()[0][0].solutions[0]

        data = {
            "captcha_0": self.request.session["turbion_captcha"].keys()[0],
            "captcha_2": solution
        }

        form = self.form_class(data=data)

        self.assert_(form.is_valid(), form.errors)

        data.update({"captcha_2": "*%s*" % solution})

        form = self.form_class(data=data)

        self.assert_(not form.is_valid(), form.errors)

    def test_form_error_report(self):
        pass

class CaptchaInvalidationTest(TestCase):
    pass
