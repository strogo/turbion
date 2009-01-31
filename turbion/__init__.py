# -*- coding: utf-8 -*-

VERSION = (0, 8, 0, 'Pushkin', 0)

def get_version():
    return ".".join(map(str, VERSION[:3])) + " " + VERSION[3]
