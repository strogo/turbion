from django.conf import settings

from turbion.core.utils.antispam.filter.akismet import Akismet

class Typepad(Akismet):
    method_map = {
        'verify-key': 'http://api.antispam.typepad.com/1.1/verify-key',
        'comment-check': 'http://%(api-key)s.api.antispam.typepad.com/1.1/comment-check',
        'submit-spam': 'http://%(api-key)s.api.antispam.typepad.com/1.1/submit-spam',
        'submit-ham': 'http://%(api-key)s.api.antispam.typepad.com/1.1/submit-ham'
    }
    key = settings.TURBION_AKISMET_API_KEY
