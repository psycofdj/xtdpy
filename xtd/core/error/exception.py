# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

class XtdException(Exception):
  def __init__(self, p_module, p_message):
    self.m_module  = p_module
    self.m_message = p_message
    super().__init__()

  def log(self):
    """todo"""
    pass

  def __str__(self):
    return "[%(module)s] %(message)s" % {
      "module" : self.m_module,
      "message" : self.m_message
    }

#------------------------------------------------------------------#

class ConfigException(XtdException):
  def __init__(self, p_message):
    super().__init__(p_module="config", p_message=p_message)


class ConfigValueException(ConfigException):
  def __init__(self, p_section, p_option, p_message):
    l_fmt = "error with parameter '%(option)s' of section '%(section)s' : %(message)s"
    l_msg = l_fmt % {
      "option" : p_option,
      "section" : p_section,
      "message" : p_message
    }
    super().__init__(l_msg)

class ConfigValueFileException(ConfigValueException):
  def __init__(self,
               p_section,
               p_option,
               p_fileName):
    l_message = "path '%s' does not name a file" % (p_fileName)
    super().__init__(p_section, p_option, l_message)


class ConfigValueDirException(ConfigValueException):
  def __init__(self,
               p_section,
               p_option,
               p_fileName):
    l_message = "path '%s' does not name a directory" % (p_fileName)
    super().__init__(p_section, p_option, l_message)


class ConfigValueDirModeException(ConfigValueException):
  def __init__(self,
               p_section,
               p_option,
               p_fileName,
               p_read = False,
               p_write = False,
               p_execute = False):
    l_modeString = ""
    if p_read:
      l_modeString += "r"
    else:
      l_modeString += "-"
    if p_write:
      l_modeString += "w"
    else:
      l_modeString += "-"
    if p_execute:
      l_modeString += "x"
    else:
      l_modeString += "-"
    l_message = "could not open directory '%s' with '%s' access" % (p_fileName, l_modeString)
    super().__init__(p_section, p_option, l_message)

class ConfigValueFileModeException(ConfigValueException):
  def __init__(self,
               p_section,
               p_option,
               p_fileName,
               p_read = False,
               p_write = False,
               p_execute = False):
    l_modeString = ""
    if p_read:
      l_modeString += "r"
    else:
      l_modeString += "-"
    if p_write:
      l_modeString += "w"
    else:
      l_modeString += "-"
    if p_execute:
      l_modeString += "x"
    else:
      l_modeString += "-"
    l_message = "could not open path '%s' with '%s' access" % (p_fileName, l_modeString)
    super().__init__(p_section, p_option, l_message)

class ConfigValueTypeException(ConfigValueException):
  INT   = "int"
  FLOAT = "float"
  BOOL  = "bool"
  def __init__(self, p_section, p_option, p_value, p_typeName):
    l_message = "could not cast value '%s' int type '%s'" % (p_value, p_typeName)
    super().__init__(p_section, p_option, l_message)

class ConfigValueLimitsException(ConfigValueException):
  def __init__(self, p_section, p_option, p_value, p_minValue = None, p_maxValue = None):
    if p_minValue is None:
      p_minValue = "-inf"
    if p_maxValue is None:
      p_maxValue = "inf"
    l_message = "value out of bounds, should be %s < %s < %s" % (p_minValue,
                                                                 p_value,
                                                                 p_maxValue)
    super().__init__(p_section, p_option, l_message)


class ConfigValueEnumException(ConfigValueException):
  def __init__(self, p_section, p_option, p_value, p_authorizedValues):
    l_message = "value '%s' must be one of the following '%s'" % (p_value, str(p_authorizedValues))
    super().__init__(p_section, p_option, l_message)
