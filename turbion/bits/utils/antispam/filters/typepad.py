from django.conf import settings

from turbion.bits.utils.antispam.filters.akismet import Akismet

class Typepad(Akismet):
    """
    Typepad filter. API docs: http://antispam.typepad.com/info/developers.html
    """
    domain = 'api.antispam.typepad.com'
    key = settings.TURBION_TYPEPAD_API_KEY
