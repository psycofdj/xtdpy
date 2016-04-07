#!/usr/bin/env python3
# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

import sys
from distutils.core import setup
from setuptools import find_packages

sys.path.insert(0, ".")

import xtd

setup(
  name         = 'xtd',
  packages     = find_packages(exclude=["*test*"]),
  version      = xtd.__version__,
  description  = xtd.__description__,
  author       = xtd.__author__.split("<")[0].strip(),
  author_email = xtd.__author__.split("<")[1].split(">")[0].strip(),
  url          = xtd.__url__,
  download_url = xtd.__download_url__,
  keywords     = xtd.__keywords__,
  classifiers  = xtd.__classifiers__
)
