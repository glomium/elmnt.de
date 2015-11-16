#!/usr/bin/python
# ex:set fileencoding=utf-8:

from setuptools import setup, find_packages
import os

CLASSIFIERS = []

VERSION = ("0","5")
__version__ = '.'.join(VERSION)
__docformat__ = 'restructuredtext'

setup(
    name='elmnt',
    version=__version__,
    packages=[],
    install_requires = [
        'pytz',
        'Pillow',

        'django>=1.8,<1.8.99',
        'django-sekizai',

        'psycopg2',
        'python-memcached',
        'python-logstash',

        'django-cms<3.1.999',
        'django-reversion',
        'django-crispy-forms<1.5',  # Version 1.5.2 has a missing template

        'djangocms-text-ckeditor',
        'djangocms-link',
        'djangocms-googlemap',
        'cmsplugin-filer',

        'easy_thumbnails',
        'django-taggit',
    ],
    include_package_data=True,
    zip_safe=False,
)
