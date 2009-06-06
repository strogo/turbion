TURBION_BLOG_NAME = "Turbion based blog"
TURBION_BLOG_POSTS_PER_PAGE = 5

TURBION_TITLE_PATTERN = '%(page)s | %(section)s | %(site)s'

TURBION_BASE_UPLOAD_PATH = "upload/turbion/"

TURBION_NOTIFICATION_FROM_EMAIL = "notifs@%(domain)s"
TURBION_NOTIFICATION_ATTEMPTS = 3

TURBION_PINGBACK_PARAGRAPH_LENGTH = 200

TURBION_ANTISPAM_FILTERS = ['trusted', 'whitelist', 'captcha', 'akismet']

TURBION_AKISMET_API_METHODS = {
    'verify-key': 'http://rest.akismet.com/1.1/verify-key',
    'comment-check': 'http://%(api-key)s.rest.akismet.com/1.1/comment-check',
    'submit-spam': 'http://%(api-key)s.rest.akismet.com/1.1/submit-spam',
    'submit-ham': 'http://%(api-key)s.rest.akismet.com/1.1/submit-ham'
}

TURBION_AKISMET_API_KEY = ''

import logging

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger('turbion').addHandler(NullHandler())
