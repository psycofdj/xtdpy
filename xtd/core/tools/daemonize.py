# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

import os
import sys
from .. import error

#------------------------------------------------------------------#

def daemonize(p_pidFilePath):
  """
  Detach a process from the controlling terminal and run it in the
  background as a daemon.
  """
  try:
    l_pid = os.fork()
  except OSError as l_exception:
    raise error.XtdError(__name__, "could not fork : %s" % str(l_exception))

  if l_pid == 0:
    os.setsid()
    try:
      l_pid = os.fork()
    except OSError as l_exception:
      raise error.XtdError(__name__, "could not fork")

    if l_pid == 0:
      os.umask(0)
      l_pidFile = open(p_pidFilePath, "w")
      l_pidFile.write(str(os.getpid()))
      l_pidFile.close()
    else:
      sys.exit(0)
  else:
    sys.exit(0)

  l_devnullFd = os.open("/dev/null", os.O_RDWR)
  os.dup2(l_devnullFd, 0)
  os.dup2(l_devnullFd, 1)
  os.dup2(l_devnullFd, 2)

def get_pid_from_file(p_fileFilePath):
  if os.path.isfile(p_fileFilePath):
    l_pidFile = open(p_fileFilePath, "r")
    l_line = l_pidFile.readline()
    try:
      l_pid = int(l_line)
    except TypeError:
      return 0
    l_pidFile.close()
    return l_pid
  return None

def is_running(p_pid):
  return os.path.isdir("/proc/%s" % p_pid)
