# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

import inspect
import sys
import logging
import importlib
import json

from .. import logger
from ..tools import mergedicts
from .. import mixin
from ..error.exception import BaseException

#------------------------------------------------------------------#

DEFAULT_CONFIG = {
  "loggers" : {
    "root" : {
      "handlers" : [ "stdout", "rotfile", "syslog"],
      "level"    : 40
    }
  },
  "handlers" : {
    "rotfile" : {
      "class"       : "logging.handlers.RotatingFileHandler",
      "filename"    : "out.log",
      "formatter"   : "default",
      "maxBytes"    : 15728640,
      "backupCount" : 3,
      "filters"     : []
    },
    "stdout" : {
      "class"       : "logging.StreamHandler",
      "formatter"   : "location",
      "stream"      : "stdout",
      "filters"     : [ "colored" ]
    },
    "syslog" : {
      "class"       : "logging.handlers.SysLogHandler",
      "formatter"   : "default",
      "address"     : "/dev/log",
      "filters"     : []
    },
    "memory" : {
      "class"       : "xtd.core.logger.handler.MemoryHandler",
      "formatter"   : "default",
      "max_records" : 2000,
      "filters"     : []
    }
  },
  "formatters" : {
    "default" : {
      "class"   : "logging.Formatter",
      "fmt"     : "%(asctime)s (%(name)s) [%(levelname)s] : %(message)s",
      "datefmt" : "%a %d %b %Y at %H-%M"
    },
    "location" : {
      "class"    : "xtd.core.logger.formatter.LocationFormatter",
      "fmt"      : "%(asctime)s (%(name)s) [%(levelname)s] : %(message)s %(location)s",
      "datefmt" : "%Y-%m-%d %H:%M:%S",
      "locfmt"   : "at %(pathname)s:%(lineno)s -> %(funcName)s",
      "locstyle" : { "colors" : [ "grey" ],  "attrs"  : [ "bold" ] }
    }
  },
  "filters" : {
    "colored" : {
      "class"   : "xtd.core.logger.filter.FieldFilter",
      "fields"  : {
        "name" : {
          "pad"    : "left",
          "styles": {
            "default" : { "colors" : [ "red"  ],  "attrs"  : [ "bold" ] }
          }
        },
        "levelname" : {
          "pad"    : "left",
          "styles" : {
            "DEBUG"     : { "colors" : [ "yellow" ],  "attrs"  : [ ]        },
            "INFO"      : { "colors" : [ "yellow" ],  "attrs"  : [ "bold" ] },
            "WARNING"   : { "colors" : [ "red" ],     "attrs"  : [ ]        },
            "ERROR"     : { "colors" : [ "red" ],     "attrs"  : [ "bold" ] },
            "EXCEPTION" : { "colors" : [ "magenta" ], "attrs"  : [ "bold" ] },
            "default"   : { "colors" : [ "yellow"  ], "attrs"  : [ "bold" ] }
          }
        }
      }
    }
  }
}


#------------------------------------------------------------------#

class WrapperLogger(logging.Logger):
  def __init__(self, p_name):
    super().__init__(p_name)

  def __sys_version(self, p_result):
    if sys.version_info.major != 2:
      return (p_result[0], p_result[1], p_result[2], None)
    return p_result

  def findCaller(self, p_stack):
    l_curFrame  = inspect.currentframe()
    l_outFrames = inspect.getouterframes(l_curFrame)
    l_sourceFrame = None
    for c_pos in range(0, len(l_outFrames)):
      l_frame, l_file, l_lineno, l_func, l_a, l_b = l_outFrames[c_pos]
      if l_file.endswith("core/logger/__init__.py") and l_func == "__wrap":
        l_sourceFrame = l_outFrames[c_pos + 2]
    if l_sourceFrame:
      return self.__sys_version((l_sourceFrame[1], l_sourceFrame[2], l_sourceFrame[3]))
    return logging.Logger.findCaller(self, p_stack)


#------------------------------------------------------------------#

class LogManager(metaclass=mixin.Singleton):
  def __init__(self):
    self.m_logs       = []
    self.m_handlers   = {}
    self.m_formatters = {}
    self.m_filters    = {}
    self.m_loggers    = {}
    self.m_config     = DEFAULT_CONFIG

  def add_formatter(self, p_name, p_obj):
    if p_name in self.m_formatters:
      raise BaseException(__name__, "multiply definied logging formatter '%s'" % p_name)
    self.m_formatters[p_name] = p_obj

  def add_filter(self, p_name, p_obj):
    if p_name in self.m_filters:
      raise BaseException(__name__, "multiply definied logging filter '%s'" % p_name)
    self.m_filters[p_name] = p_obj

  def add_handler(self, p_name, p_obj):
    if p_name in self.m_handlers:
      raise BaseException(__name__, "multiply definied logging handler '%s'" % p_name)
    self.m_handlers[p_name] = p_obj

  def get_formatter(self, p_name):
    if not p_name in self.m_formatters:
      raise BaseException(__name__, "undefinied logging formatter '%s'" % p_name)
    return self.m_formatters[p_name]

  def get_filter(self, p_name):
    if not p_name in self.m_filters:
      raise BaseException(__name__, "undefinied logging filter '%s'" % p_name)
    return self.m_filters[p_name]

  def get_handler(self, p_name):
    if not p_name in self.m_handlers:
      raise BaseException(__name__, "undefinied logging handler '%s' " % p_name)
    return self.m_handlers[p_name]

  def _get_class(self, p_name):
    l_parts      = p_name.split('.')
    l_moduleName = '.'.join(l_parts[:-1])
    l_className  = '.'.join(l_parts[-1:])
    try:
      l_module = importlib.import_module(l_moduleName)
    except Exception as l_error:
      raise BaseException(__name__, "unable to import module '%s' : %s" % (l_moduleName, str(l_error)))

    try:
      return getattr(l_module, l_className)
    except Exception as l_error:
      raise BaseException(__name__, "unable to find class '%s' in module '%s'" % (l_className, l_moduleName))

  def load_config(self, p_config, p_override):
    l_config = p_config
    if l_config == {}:
      l_config = self.m_config
    try:
      l_result = dict(mergedicts.mergedicts(l_config, p_override))
      self.m_config = l_result
    except Exception as l_error:
      raise BaseException(__name__, "unable to override logging configuration '%s' : %s" % (str(p_override), str(l_error)))

  def _load_filters(self):
    l_usedFilters = set()
    for c_name, c_value in self.m_config["handlers"].items():
      l_usedFilters |= set([ x for x in c_value["filters"] ])
    l_filters = { x:y for x,y in self.m_config["filters"].items() if x in l_usedFilters }
    for c_name, c_conf in l_filters.items():
      l_class = self._get_class(c_conf["class"])
      l_params = { x : y for x,y in c_conf.items() if x != "class" }
      try:
        l_obj = l_class(**l_params)
      except Exception as l_error:
        raise BaseException(__name__, "unable to initialize logging filter '%s' : %s" % (c_name, str(l_error)))
      self.add_filter(c_name, l_obj)

  def _load_formatters(self):
    l_usedFormatters = set([ y["formatter"] for x,y in self.m_config["handlers"].items() ])
    l_formatters     = { x:y for x,y in self.m_config["formatters"].items() if x in l_usedFormatters }
    for c_name, c_conf in l_formatters.items():
      l_class  = self._get_class(c_conf["class"])
      l_params = { x : y for x,y in c_conf.items() if x != "class" }
      try:
        l_obj = l_class(**l_params)
      except Exception as l_error:
        raise BaseException(__name__, "unable to initialize logging formatter '%s' : %s" % (c_name, str(l_error)))
      self.add_formatter(c_name, l_obj)

  def _load_handlers(self):
    l_usedHandlers = set()
    for c_name, c_value in self.m_config["loggers"].items():
      l_usedHandlers |= set([ x for x in c_value["handlers"] ])
    l_handlers = { x:y for x,y in self.m_config["handlers"].items() if x in l_usedHandlers }
    for c_name, c_conf in l_handlers.items():
      l_class = self._get_class(c_conf["class"])
      l_formatterName = c_conf.get("formatter", "default")
      l_params = { x : y for x,y in c_conf.items() if x not in [ "class", "formatter", "filters" ] }
      if "stream" in l_params:
        if l_params["stream"] == "stdout":
          l_params["stream"] = sys.stdout
        elif l_params["stream"] == "stderr":
          l_params["stream"] = sys.stderr
        else:
          l_params["stream"] = open(l_params["stream"], mode="w+")
      try:
        l_obj = l_class(**l_params)
      except Exception as l_error:
        raise BaseException(__name__, "unable to initialize logging handler '%s' : %s" % (c_name, str(l_error)))
      l_formatter = self.get_formatter(l_formatterName)
      l_obj.setFormatter(l_formatter)
      for c_filter in c_conf.get("filters", []):
        l_filter = self.get_filter(c_filter)
        l_obj.addFilter(l_filter)
      self.add_handler(c_name, l_obj)

  def _load_loggers(self):
    for c_name, c_conf in self.m_config["loggers"].items():
      l_handlers = c_conf.get("handlers", [])
      l_level    = c_conf.get("level", 40)
      if c_name == "root":
        l_logger = logging.getLogger()
      else:
        l_logger = logging.getLogger(c_name)
      l_logger.setLevel(l_level)
      for c_handler in l_handlers:
        l_handler = self.get_handler(c_handler)
        l_logger.addHandler(l_handler)

  def initialize(self, p_config = {}, p_override = {}):
    logging.setLoggerClass(WrapperLogger)
    self.load_config(p_config, p_override)
    try:
      self._load_filters()
      self._load_formatters()
      self._load_handlers()
      self._load_loggers()
    except KeyError as l_error:
      raise BaseException(__name__, "unable to initialize logging facility : unexpected key %s in configuration" % str(l_error))
    except Exception as l_error:
      raise BaseException(__name__, "unable to initialize logging facility : %s" % str(l_error))
    logger.info(__name__, "facility initialized")
