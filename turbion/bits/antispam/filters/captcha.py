from django.conf.urls.defaults import patterns, url
from django.utils.translation import ugettext_lazy as _

from supercaptcha import CaptchaField

from turbion.bits.antispam import Filter

class Captcha(Filter):
    urlpatterns = patterns('',
        url(r'^captcha/(?P<code>[\da-f]{32})/$', 'supercaptcha.draw'),
    )

    def process_form_init(self, request, form, parent=None):
        form.fields['captcha'] = CaptchaField(label=_('check'))


