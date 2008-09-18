# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

class ImageWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        return mark_safe(forms.HiddenInput().render(name, value) + u'<img src=\"%s\" width="150" heigth="60"/> ' % value)

class CaptchaWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (forms.HiddenInput(),
                   ImageWidget(),
                   forms.TextInput(),
                )
        self._test_id = None
        super(CaptchaWidget, self).__init__(widgets, attrs)

    def render(self, name, value, attrs=None):
        return mark_safe('<div class="captcha_fieldset">%s</div><div class="after_captcha"></div>' % super(CaptchaWidget, self).render(name, value, attrs))

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
    widget = CaptchaWidget

    def __init__(self, request, *args, **kwargs):
        from turbion.utils.captcha import CaptchaManager

        self.request = request
        self.manager = CaptchaManager(self.request)

        super(CaptchaField, self).__init__(*args, **kwargs)
        self.widget.manager = self.manager

    def clean(self, value):
        id = str(value[0])
        word = value[2]

        test = self.manager.get_test(id)
        if not test:
            raise forms.ValidationError("Recognition error")
        elif not test.valid:
            raise forms.ValidationError("Recognition error")
        elif not test.testSolutions([word]):
            raise forms.ValidationError("Word was recognized incorrect")

        return value
