from django.conf import settings

from turbion.core.utils.antispam.filter.akismet import Akismet

class Typepad(Akismet):
    """
    Typepad filter. API docs: http://antispam.typepad.com/info/developers.html
    """
    domain = 'api.antispam.typepad.com'
    key = settings.TURBION_AKISMET_API_KEY
