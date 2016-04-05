# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

import logging

#------------------------------------------------------------------#

def get(p_module = None):
  if (p_module == "root") or (p_module is None):
    return logging.getLogger()
  return logging.getLogger(p_module)

def __wrap(p_func, p_module, p_msg, *p_args, **p_kwds):
  l_logger = logging.getLogger(p_module)
  l_func   = getattr(l_logger, p_func)
  l_func(p_msg, *p_args, **p_kwds)

def debug(p_module, p_msg, *p_args, **p_kwds):
  __wrap("debug", p_module, p_msg, *p_args, **p_kwds)
def info(p_module, p_msg, *p_args, **p_kwds):
  __wrap("info", p_module, p_msg, *p_args, **p_kwds)
def warning(p_module, p_msg, *p_args, **p_kwds):
  __wrap("warning", p_module, p_msg, *p_args, **p_kwds)
def error(p_module, p_msg, *p_args, **p_kwds):
  __wrap("error", p_module, p_msg, *p_args, **p_kwds)
def critical(p_module, p_msg, *p_args, **p_kwds):
  __wrap("critical", p_module, p_msg, *p_args, **p_kwds)
def exception(p_module, p_msg, *p_args, **p_kwds):
  __wrap("exception", p_module, p_msg, *p_args, **p_kwds)
def log(p_level, p_module, p_msg, *p_args, **p_kwds):
  __wrap(p_level, p_module, p_msg, *p_args, **p_kwds)

#------------------------------------------------------------------#
