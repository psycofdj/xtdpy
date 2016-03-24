#!/usr/bin/env python3
# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

from distutils.core import setup
from setuptools import find_packages

setup(
  name         = 'xtd',
  packages     = find_packages(exclude=["*test*"]),
  version      = '0.1',
  description  = 'High level library to quickly build strong python apps',
  author       = 'Xavier MARCELET',
  author_email = 'xavier@marcelet.com',
  url          = 'https://github.com/psycofdj/xtd',
  download_url = 'https://github.com/psycofdj/xtd/tarball/0.1',
  keywords     = ['python', 'high-level'],
  classifiers  = [],
)
