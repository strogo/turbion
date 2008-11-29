# -*- coding: utf-8 -*-
from django.test import TestCase
from django import forms
from django import http

from turbion.utils.testing import RequestFactory
from turbion.utils.captcha.storage import CaptchaManager
from turbion.utils.captcha.forms import CaptchaField
from turbion.utils.captcha.utils import get_solution

class CaptchaImageTest(TestCase):
    def setUp(self):
        self.session = {}

        session_store = CaptchaManager(self.session)
        self.test = session_store.make_test()

    def test_image_generation(self):
        response = http.HttpResponse(mimetype ='image/jpeg')
        CaptchaManager(self.session).render_test(response, self.test.id)

        self.assertEqual(
            response.status_code,
            200
        )

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
