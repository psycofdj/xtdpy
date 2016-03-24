# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

import urllib
import json
import os
import re
import socket
from functools import partial

from ..error.exception import *
from ..tools           import url

#------------------------------------------------------------------#


def check_file(p_section, p_name, p_value, p_read = False, p_write = False, p_execute = False):
  l_absFilePath = os.path.expanduser(p_value)
  l_absFilePath = os.path.abspath(l_absFilePath)

  if os.path.isdir(l_absFilePath):
    raise ConfigValueFileException(p_section, p_name, l_absFilePath)

  if not os.path.exists(l_absFilePath):
    if p_read or not check_mode(os.path.dirname(l_absFilePath), p_write=True):
      raise ConfigValueFileModeException(p_section, p_name, p_value, p_read, p_write, p_execute)
  else:
    if not check_mode(l_absFilePath, p_read, p_write, p_execute):
      raise ConfigValueFileModeException(p_section, p_name, p_value, p_read, p_write,p_execute)
  return l_absFilePath

# ------------------------------------------------------------------------- #

def check_dir(p_section, p_name, p_value, p_read = False, p_write = False, p_execute = False):
  l_absDirPath = os.path.expanduser(p_value)
  l_absDirPath = os.path.abspath(l_absDirPath)
  if not os.path.isdir(l_absDirPath):
    raise ConfigValueDirException(p_section, p_name, l_absDirPath)
  if not check_mode(l_absDirPath, p_read, p_write, p_execute):
    raise ConfigValueDirModeException(p_section, p_name, p_value, p_read, p_write, p_execute)
  return l_absDirPath

# ------------------------------------------------------------------------- #

def check_int(p_section, p_name, p_value, p_min = None, p_max = None):
  if type(p_value) == int:
    l_value = p_value
  else:
    if type(p_value) == str:
      try:
        l_value = int(p_value)
      except ValueError:
        raise ConfigValueTypeException(p_section, p_name, p_value, ConfigValueTypeException.INT)
    else:
      raise ConfigValueTypeException(p_section, p_name, p_value, ConfigValueTypeException.INT)

  if (p_min != None) and (l_value < p_min):
    raise ConfigValueLimitsException(p_section, p_name, l_value, p_min, p_max)
  if (p_max != None) and (l_value > p_max):
    raise ConfigValueLimitsException(p_section, p_name, l_value, p_min, p_max)
  return l_value

# ------------------------------------------------------------------------- #

def check_float(p_section, p_name, p_value, p_min = None, p_max = None):
  if type(p_value) == float:
    l_value = p_value
  else:
    if type(p_value) == str:
      try:
        l_value = float(p_value)
      except ValueError:
        raise ConfigValueTypeException(p_section, p_name, p_value, ConfigValueTypeException.FLOAT)
    else:
      raise ConfigValueTypeException(p_section, p_name, p_value, ConfigValueTypeException.FLOAT)
  if (p_min != None) and (l_value < p_min):
    raise ConfigValueLimitsException(p_section, p_name, l_value, p_min, p_max)
  if (p_max != None) and (l_value > p_max):
    raise ConfigValueLimitsException(p_section, p_name, l_value, p_min, p_max)
  return l_value

# ------------------------------------------------------------------------- #

def check_bool(p_section, p_name, p_value):
  if type(p_value) == bool:
    return p_value
  if type(p_value) != str:
    raise ConfigValueTypeException(p_section, p_name, p_value, ConfigValueTypeException.BOOL)
  if ((p_value.lower() == 'true') or
      (p_value.lower() == 'yes') or
      (p_value.lower() == 'on')):
    return True
  if ((p_value.lower() == 'false') or
      (p_value.lower() == 'no') or
      (p_value.lower() == 'off')):
    return False
  raise ConfigValueTypeException(p_section, p_name, p_value, ConfigValueTypeException.BOOL)

# ------------------------------------------------------------------------- #

def check_enum(p_section, p_name, p_value, p_values):
  if not p_value in p_values:
    raise ConfigValueEnumException(p_section, p_name, p_value, p_values)
  return p_value

# ------------------------------------------------------------------------- #

def check_mode(p_path, p_read = False, p_write = False, p_execute = False):
  if not os.path.exists(p_path):
      return False
  l_mode = os.F_OK
  if p_read:
    l_mode = l_mode or os.R_OK
  if p_write:
    l_mode = l_mode or os.W_OK
  if p_execute:
    l_mode = l_mode or os.X_OK
  if os.access(p_path, l_mode):
    return True
  return False

# ------------------------------------------------------------------------- #


def check_mail(p_section, p_name, p_value):
  l_mail_regexp = "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"
  if not re.match("^%s$" % l_mail_regexp, p_value):
    if not re.match("^[^<]*<%s>$" % l_mail_regexp, p_value):
      l_message = "value '%s' is not an email address" % p_value
      raise ConfigValueException(p_section, p_name, l_message)
  return p_value

# ------------------------------------------------------------------------- #

def check_array(p_section, p_name, p_value, p_check = None):
  l_res   = []
  l_value = p_value
  if not type(l_value) == list:
    l_value = l_value.split(",")
  for c_val in l_value:
    if p_check:
      l_res.append(p_check(p_section, p_name, c_val))
    else:
      l_res.append(c_val)
  return l_res

# ------------------------------------------------------------------------- #

def check_host(p_section, p_name, p_value):
  try:
    socket.gethostbyname(p_value)
  except socket.gaierror:
    l_message = "host '%s' is not valid" % p_value
    raise ConfigValueException(p_section, p_name, l_message)
  return p_value

# ------------------------------------------------------------------------- #

def check_json(p_section, p_name, p_value, p_checks = {}):
  if type(p_value) != dict:
    try:
      p_value = json.loads(p_value)
    except Exception as l_error:
      raise ConfigValueException(p_section, p_name, "invalid json : %s" % str(l_error))
  return p_value

# ------------------------------------------------------------------------- #

def check_socket(p_section, p_name, p_value, p_schemes = [], p_checkUnix = False):
  l_parts = urllib.parse.urlparse(p_value)
  if len(p_schemes) and (not l_parts[0] in p_schemes):
    raise ConfigValueException(p_section, p_name, "invalid url '%s', scheme '%s' not in '%s'" % (p_value, l_parts[0], str(p_schemes)))

  l_url, l_unix = url.parse_unix(p_value)
  if p_checkUnix and l_unix:
    check_file(p_section, p_name, l_unix, p_read=True, p_write=True)
  return p_value

# ------------------------------------------------------------------------- #

def is_file(*p_args, **p_kwds):
  return partial(check_file, *p_args, **p_kwds) # pragma: no cover
def is_dir(*p_args, **p_kwds):
  return partial(check_dir, *p_args, **p_kwds) # pragma: no cover
def is_int(*p_args, **p_kwds):
  return partial(check_int, *p_args, **p_kwds) # pragma: no cover
def is_float(*p_args, **p_kwds):
  return partial(check_float, *p_args, **p_kwds) # pragma: no cover
def is_bool(*p_args, **p_kwds):
  return partial(check_bool, *p_args, **p_kwds) # pragma: no cover
def is_enum(*p_args, **p_kwds):
  return partial(check_enum, *p_args, **p_kwds) # pragma: no cover
def is_mail(*p_args, **p_kwds):
  return partial(check_mail, *p_args, **p_kwds) # pragma: no cover
def is_array(*p_args, **p_kwds):
  return partial(check_array, *p_args, **p_kwds) # pragma: no cover
def is_host(*p_args, **p_kwds):
  return partial(check_host, *p_args, **p_kwds) # pragma: no cover
def is_json(*p_args, **p_kwds):
  return partial(check_json, *p_args, **p_kwds) # pragma: no cover
def is_socket(*p_args, **p_kwds):
  return partial(check_socket, *p_args, **p_kwds) # pragma: no cover

# ------------------------------------------------------------------------- #
