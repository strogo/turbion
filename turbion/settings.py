TURBION_BLOG_NAME = "Turbion based blog"
TURBION_BLOG_POSTS_PER_PAGE = 5
TURBION_ADDITIONAL_POST_FIELDS = False

TURBION_TITLE_PATTERN = '%(page)s | %(section)s | %(site)s'

TURBION_BASE_UPLOAD_PATH = "upload/turbion/"

TURBION_NOTIFACTIONS_FROM_EMAIL = "notifs@%(domain)s"

TURBION_USE_SUPERCAPTCHA = True

TURBION_PINGBACK_PARAGRAPH_LENGTH = 200

import logging

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger('turbion').addHandler(NullHandler())
