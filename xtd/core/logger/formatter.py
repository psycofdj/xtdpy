# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

import logging
import termcolor

#------------------------------------------------------------------#

class LocationFormatter(logging.Formatter):
  def __init__(self,
               fmt      = "%(asctime)s (%(name)s) [%(levelname)s] : %(message)s %(location)s",
               datefmt  = "%Y-%m-%d %H:%M:%S",
               locfmt   = "at %(pathname)s:%(lineno)s -> %(funcName)s",
               locstyle = None):
    super().__init__(fmt, datefmt)
    self.m_fmt      = fmt
    self.m_locFmt   = locfmt
    self.m_datefmt  = datefmt
    self.m_locstyle = locstyle

    if locstyle is None:
      self.m_locstyle = { "colors" : [], "attrs" : [] }

  def _get_loc(self, p_record):
    l_loc = self.m_locFmt % { x : getattr(p_record, x) for x in dir(p_record) if x[0] != "_" }
    l_args = {}
    l_colors = self.m_locstyle.get("colors", [])
    l_attrs  = self.m_locstyle.get("attrs",  [])
    if not isinstance(l_colors, list):
      l_colors = [ l_colors ]
    if not isinstance(l_attrs, list):
      l_attrs = [ l_attrs ]
    l_args["attrs"] = l_attrs
    for c_color in l_colors:
      if c_color[0:3] == "on_":
        l_args["on_color"] = c_color
      else:
        l_args["color"] = c_color
    return termcolor.colored(l_loc, **l_args)

  def format(self, p_record):
    l_loc = self._get_loc(p_record)
    self._style._fmt = self.m_fmt.replace("%(location)s", l_loc)
    return super().format(p_record)
