# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

import inspect

#------------------------------------------------------------------#

class Singleton(type):
  ms_instances = {}
  def __call__(p_class, *p_args, **p_kwargs):
    if p_class not in p_class.ms_instances:
      p_class.ms_instances[p_class] = super(Singleton, p_class).__call__(*p_args, **p_kwargs)
    return p_class.ms_instances[p_class]

  @classmethod
  def reset(p_class, p_item):
    if p_item in p_class.ms_instances:
      del p_class.ms_instances[p_item]

#------------------------------------------------------------------#

