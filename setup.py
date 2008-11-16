from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
    name = "Turbion",
    version = "0.6",
    packages = find_packages(),

    scripts = ['turbion/bin/turbion-admin.py'],

    install_requires = [
        'Imaging>=1.1.6',
        'Pytils',
    ],

    author = "Alex Koshelev",
    author_email = "daevaorn@gmail.com",
    description = "Flexible django-based blog application",
    license = "New BSD",
    url = "http://turbion.org/",
)
