#!/usr/bin/env python
from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages, findall

from version import get_version

def strip_turbion(paths):
    return [p[len('turbion/'):] for p in paths]

setup(
    name = "turbion",
    version = get_version('0.8'),
    packages = find_packages(),

    package_data={
        'turbion': strip_turbion(findall('turbion/locale')) +\
                   strip_turbion(findall('turbion/templates')) +\
                   strip_turbion(findall('turbion/fixtures')) +\

                   strip_turbion(findall('turbion/contrib/openid/templates')) +\
                   strip_turbion(findall('turbion/contrib/feedback/fixtures'))
    },

    author = "Alex Koshelev",
    author_email = "daevaorn@gmail.com",
    description = "Flexible django-based blog application",
    license = "New BSD",
    url = "http://turbion.org/",
)
