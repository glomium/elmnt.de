#!/usr/bin/python
# ex:set fileencoding=utf-8:

from setuptools import setup
from setuptools import find_packages
import os

CLASSIFIERS = []

VERSION = ("0","9", "0")
NAME = os.path.basename(os.path.abspath(os.path.dirname(__file__)))

__version__ = '.'.join(VERSION)
__docformat__ = 'restructuredtext'

requirements_base = list([req.strip() for req in open(
    os.path.join(os.path.dirname(__file__), 'requirements_base.txt')
).readlines()])

requirements_custom = list([req.strip() for req in open(
    os.path.join(os.path.dirname(__file__), 'requirements_custom.txt')
).readlines()])

setup(
    name=NAME,
    version=__version__,
    packages=[],
    install_requires=requirements_base+requirements_custom,
    include_package_data=True,
    zip_safe=False,
)
