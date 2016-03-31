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
  version      = '0.2',
  description  = 'High level library to quickly build strong python apps',
  author       = 'Xavier MARCELET',
  author_email = 'xavier@marcelet.com',
  url          = 'https://github.com/psycofdj/xtd',
  download_url = 'https://github.com/psycofdj/xtd/tarball/0.2',
  keywords     = ['xtd', 'python', 'library', 'high-level'],
  classifiers  = [
    "Development Status :: 2 - Pre-Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: Unix",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Software Development :: Libraries :: Python Modules"
  ],
)
