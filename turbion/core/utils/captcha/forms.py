# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

class ImageWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        return mark_safe(
                     u'<img src=\"%s\" width="150" heigth="60"/> ' % value
        )

class CaptchaWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.HiddenInput(),
            ImageWidget(),
            forms.TextInput(),
        )
        self._test_id = None
        super(CaptchaWidget, self).__init__(widgets, attrs)

    @property
    def initial(self):
        test = self.manager.make_test()
        self._test_id = test.id

        return (test.id, reverse('turbion_captcha_image', kwargs={"id": test.id}))

    def render(self, name, value, attrs=None):
        if isinstance(value, (list, tuple)):
            value = list(value)
            value[1] = reverse('turbion_captcha_image', kwargs={"id": value[0]})

        return super(CaptchaWidget, self).render(name, value, attrs)

    def decompress(self, value):
        return self.initial

    def get_id(self):
        return self._test_id

class CaptchaField(forms.Field):
    widget = CaptchaWidget

    def __init__(self, request, *args, **kwargs):
        from turbion.core.utils.captcha import CaptchaManager

        self.manager = CaptchaManager(request.session)

        super(CaptchaField, self).__init__(*args, **kwargs)
        self.widget.manager = self.manager

    def clean(self, value):
        id, image, word = value

        test = self.manager.get_test(id)

        if not test:
            raise forms.ValidationError("Recognition error")
        elif not test.valid:
            raise forms.ValidationError("Recognition error")
        elif not test.testSolutions([word]):
            raise forms.ValidationError("Word was recognized incorrect")

        return (id, image, word)