# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

from . import writter, handler, counter, manager

#------------------------------------------------------------------#

def get(p_name):
  from .manager import StatManager
  return StatManager().get(p_name)
