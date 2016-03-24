# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

from .manager import StatManager

#------------------------------------------------------------------#

def get(p_name):
  return CounterManager().get(p_name);
