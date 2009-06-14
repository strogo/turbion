from django.conf import settings

from turbion.core.utils.antispam.filter.akismet import Akismet

class Typepad(Akismet):
    domain = 'api.antispam.typepad.com'
    key = settings.TURBION_AKISMET_API_KEY
