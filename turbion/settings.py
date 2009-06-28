TURBION_BLOG_NAME = "Turbion based blog"
TURBION_BLOG_POSTS_PER_PAGE = 5

TURBION_TITLE_PATTERN = '%(page)s | %(section)s | %(site)s'

TURBION_BASE_UPLOAD_PATH = "upload/turbion/"

TURBION_NOTIFICATION_FROM_EMAIL = "notifs@%(domain)s"
TURBION_NOTIFICATION_ATTEMPTS = 3

TURBION_ANTISPAM_FILTERS = ['trusted', 'whitelist', 'captcha', 'akismet', 'typepad']

TURBION_AKISMET_API_KEY = ''
TURBION_TYPEPAD_API_KEY = ''

import logging

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger('turbion').addHandler(NullHandler())
