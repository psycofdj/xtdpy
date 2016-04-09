# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

import time
import sys
import os
import termcolor
import unittest

from xtd.core.stat.handler import BaseHandler, DiskHandler, HttpHandler


#------------------------------------------------------------------#


class BaseHandlerTest(unittest.TestCase):
  def __init__(self, *p_args, **p_kwds):
    super().__init__(*p_args, **p_kwds)

  def test_write(self):
    l_val = BaseHandler("toto")
    with self.assertRaises(NotImplementedError):
      l_val.write({})

  def test_work(self):
    l_val = BaseHandler("toto")
    with self.assertRaises(NotImplementedError):
      l_val.write({})
