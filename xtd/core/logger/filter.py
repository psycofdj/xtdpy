# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

import logging
import termcolor

#------------------------------------------------------------------#

class FieldFilter(logging.Filter):
  def __init__(self, fields):
    super().__init__()
    self.m_fields = fields
    self.m_widths = { x : 0 for x in fields.keys() }

  def _pad(self, p_record):
    l_data = { x:y for x,y in self.m_fields.items() if y.get("pad", False) }
    for c_name, c_data in l_data.items():
      l_value = getattr(p_record, c_name)
      l_size  = len(l_value)
      self.m_widths[c_name] = max(self.m_widths[c_name], l_size)
      if c_data["pad"] == "right":
        l_format = "%%-%ds" % self.m_widths[c_name]
      else:
        l_format = "%%%ds" % self.m_widths[c_name]
      l_value = l_format % l_value
      setattr(p_record, c_name, l_value)

  def _color(self, p_record):
    l_data = { x:y for x,y in self.m_fields.items() if y.get("styles", None ) }
    for c_name, c_data in l_data.items():
      try:
        l_value = getattr(p_record, c_name)
      except:
        continue

      l_values = c_data.get("styles", { "default" : { "colors" : [], "attrs" : [] } })
      if l_value in l_values.keys():
        l_style = l_values[l_value]
      else:
        l_style = l_values["default"]

      l_args = {}
      for c_color in l_style["colors"]:
        if c_color[0:3] == "on_":
          l_args["on_color"] = c_color
        else:
          l_args["color"] = c_color
      l_args["attrs"] = l_style.get("attrs", [])
      l_value = termcolor.colored(l_value, **l_args)
      setattr(p_record, c_name, l_value)

  def filter(self, p_record):
    self._pad(p_record)
    self._color(p_record)
    return True
