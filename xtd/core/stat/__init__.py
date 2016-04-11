# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

from . import handler, counter, manager

#------------------------------------------------------------------#

def get(p_ns, p_name):
  from .manager import StatManager
  return StatManager().get(p_ns, p_name)
