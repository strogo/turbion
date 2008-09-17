# -*- coding: utf-8 -*-
from django.test import TestCase
from django import http

class BaseViewTest(TestCase):
    def assertStatus(self, url, status=http.HttpResponse.status_code):
        response = self.client.get(url)

        self.assertEqual(response.status_code, status)

        return response
