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

        'django>=1.7,<1.7.99',
        'django-sekizai',

        'psycopg2',
        'python-memcached',
        'python-logstash',

#       'uwsgi',
        'uwsgidecorators',

        'django-reversion',
        'django-cms<3.0.999',
        'django-crispy-forms',

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
