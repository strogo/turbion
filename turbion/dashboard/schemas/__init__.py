# -*- coding: utf-8 -*-
import re
import os

from turbion.dashboard.schemas.base import SchemaSpot, Schema

EXCLUDE = ["__init__.py", "base.py"]
PYTHON_FILE_RE = re.compile("^.+\.py$")

for path in os.listdir(os.path.dirname(os.path.normpath(__file__))):
    name = ".".join(path.split('.')[-2:])
    if name not in EXCLUDE and PYTHON_FILE_RE.match(name):
        name = name.split('.')[-2]
        __import__("turbion.dashboard.schemas.%s" % name, {}, {}, [""])
