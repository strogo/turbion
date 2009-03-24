#!/usr/bin/env python
from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

# assume that it is relative import
from turbion import get_version

setup(
    name = "turbion",
    version = get_version(),
    packages = find_packages(),

    scripts = ['turbion/bin/turbion-admin.py'],

    install_requires = [
        'Pytils',
        'markdown2>=1.0.1.11'
    ],

    author = "Alex Koshelev",
    author_email = "daevaorn@gmail.com",
    description = "Flexible django-based blog application",
    license = "New BSD",
    url = "http://turbion.org/",
)
