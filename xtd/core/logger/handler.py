# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

import logging

#------------------------------------------------------------------#

class MemoryHandler(logging.Handler):
  def __init__(self, max_records):
    super().__init__()
    self.m_max_records = max_records



