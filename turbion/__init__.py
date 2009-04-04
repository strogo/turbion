import logging

VERSION = (0, 8, 2, 'Pushkin', 0)

def get_version():
    return ".".join(map(str, VERSION[:3])) + " " + VERSION[3]

logger = logging.getLogger('turbion')
