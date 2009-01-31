import os

TURBION_BASE_PATH = os.path.normpath(os.path.dirname(__file__))

TURBION_BLOGS_MULTIPLE = False
TURBION_TITLE_PATTERN = '%(page)s | %(section)s | %(site)s'

TURBION_BASE_UPLOAD_PATH = "upload/turbion/"

TURBION_NOTIFACTIONS_FROM_EMAIL = "notifs@%(domain)s"
