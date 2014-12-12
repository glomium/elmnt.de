#!/usr/bin/python
# ex:set fileencoding=utf-8:

from setuptools import setup, find_packages
import os

CLASSIFIERS = []

VERSION = ("0","4")
__version__ = '.'.join(VERSION)
__docformat__ = 'restructuredtext'

setup(
    name='elmnt',
    version=__version__,
    packages=[],
    install_requires = [
        'pytz',
        'Pillow',
        'django',
        'django>=1.7,<1.8',
        'django-sekizai',
        'uwsgi',

        'django-reversion',
        'django-cms',

        'djangocms-text-ckeditor',
        'djangocms-link',
        'djangocms-googlemap',
        'cmsplugin-filer',

#        # ERP
#       'django-mptt',
#       'django-filter',
#       'reportlab<3.0',
#       'xhtml2pdf',

#       'django-celery==3.0.10',
#       'kombu==2.4.7',
#       'billiard==2.7.3.17',
#       'celery==3.0.11',
#       'amqplib==1.0.2',

        'python-memcached',

        'easy_thumbnails',
        'django-taggit',
    ],
    include_package_data=True,
    zip_safe=False,
)
