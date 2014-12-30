#!/usr/bin/python
# ex:set fileencoding=utf-8:

from setuptools import setup, find_packages

setup(
    name='cmsplugin_bootstrap',
    version='0.2.0',
    url="http://igelware.de",
    license='BSD',
    platforms=['OS Independent'],
    author="Sebastian Braun",
    author_email="sebastian@elmnt.de",
    packages=find_packages(),
    install_requires=[
        'django',
    ],
    include_package_data=True,
    zip_safe=False,
)
