# -*- coding: utf-8 -*-
import re

from django.forms import fields
from django import forms
from django.forms.util import ValidationError
from django.utils.translation import ugettext

from django.forms.widgets import Widget, HiddenInput, TextInput
from pantheon.supernovaforms import captcha
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

class ImageWidget(Widget):
    def render(self, name, value, attrs=None):
        return mark_safe(HiddenInput().render(name, value) + u'<img src=\"%s\" width="150" heigth="60"/> ' % value)

class CaptchaWidget(MultiWidget):
    def __init__(self, attrs=None):
        widgets = (HiddenInput(),
                   ImageWidget(),
                   TextInput(),
                )
        self._test_id = None
        super(CaptchaWidget, self).__init__(widgets, attrs)

    def render(self, name, value, attrs=None):
        return mark_safe('<div class="captcha_fieldset">%s</div><div class="after_captcha"></div>' %  super(CaptchaWidget, self).render(name, value, attrs))

    def decompress(self, value):
        # id    - 0
        # image - 1
        # word  - 2
        test = self.manager.make_test()
        self._test_id = test.id
        value = (test.id, reverse('captcha_image', kwargs={"id": test.id}))
        return value

    def get_id(self):
        return self._test_id

class CaptchaField(forms.Field):
    widget = widgets.CaptchaWidget
    
    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.manager = CaptchaManager(self.request)
        
        super(CaptchaField, self).__init__(*args, **kwargs)
        self.widget.manager = self.manager
    
    def clean(self, value):
        from turbion.utils.captcha import CaptchaManager

        id = str(value[0])
        word = value[2]

        test = self.manager.get_test(id)
        if not test:
            raise ValidationError("Recognizing error")
        elif not test.valid:
            raise ValidationError("Recognizing error")
        elif not test.testSolutions([word]):
            raise ValidationError("Word recognized incorrect")

        return value