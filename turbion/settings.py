import os

TURBION_BASE_PATH = os.path.normpath(os.path.dirname(__file__))

TURBION_BLOG_NAME = "Turbion based blog"
TURBION_BLOG_POSTS_PER_PAGE = 5
TURBION_ADDITIONAL_POST_FIELDS = False

TURBION_TITLE_PATTERN = '%(page)s | %(section)s | %(site)s'

TURBION_BASE_UPLOAD_PATH = "upload/turbion/"

TURBION_NOTIFACTIONS_FROM_EMAIL = "notifs@%(domain)s"

TURBION_CONTRIB_GLOBAL_ADMIN = True

TURBION_USE_SUPERCAPTCHA = True
