# -*- coding: utf-8 -*-

import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 6):
    raise RuntimeError("It requires Python 3.6+")

name = "trpc_wecar_roi_s_app_wecar_roi_dmtree"
version = "0.1.0"
packages = find_packages()

setup(
    name=name,
    version=version,
    packages=packages,
    author='',
    author_email='',
    maintainer='',
    maintainer_email='',
    url='',
    license='',
    description='',
    package_data={'': ['*.proto']},

)
