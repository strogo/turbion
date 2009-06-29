from django.contrib.sites.models import Site
from django.utils.encoding import smart_unicode
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

def gen_title(bits, pattern=None):
    domain = Site.objects.get_current().domain

    pattern = pattern or settings.TURBION_TITLE_PATTERN

    defaults = {
        "page": _("Page"),
        "section": _("Section"),
        "site": domain
    }
    defaults.update(bits)

    return smart_unicode(pattern) % defaults
