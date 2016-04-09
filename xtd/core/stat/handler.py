# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

import abc
import os
import requests

from .manager       import StatManager
from ..tools.thread import SafeThread
from ..error        import XtdError
from ..             import logger

#------------------------------------------------------------------#

class BaseHandler(SafeThread):
  """ Abstract statistic handler

  Spawns a dedicated thread that outputs counters registered in the
  :py:class:`~xtd.core.stat.manager.StatManager` singleton  every
  ``p_interval`` seconds.

  User should inherit this class and define :py:meth:`write` method

  Args:
    p_name (str): handler name
    p_interval (int) : interval, in second, between two outputs
  """
  def __init__(self, p_name, p_interval = 50):
    super().__init__(p_name, p_interval)

  @abc.abstractmethod
  def write(self, p_counters):
    """ Ouput available counter data (abstract)

    Args:
      p_counters (dict): dictionary holding all available counters assiciated with
       their namespace. ``{ "<counter_namespace>" : <counter_object> }``
    """
    raise NotImplementedError

  def work(self):
    """ Output available counter data

    Implementation of :py:meth:`xtd.core.tools.thread.SafeThread.work`
    """
    l_data = StatManager().get_all()
    self.write(l_data)


#------------------------------------------------------------------#


class DiskHandler(BaseHandler):
  """ Output counters to filesystem

  Given :

   - a counter named ``counter.name`` of value ``55``
   - registered in :py:class:`xtd.core.stat.manager.StatManager` with namespace ``a.b.c``
   - a DiskHandler constructed with ``/var/snmp``

  This will create a file ``/var/snmp/a/b/c/counter.name`` containing the string ``55``


  Args:
    p_directory (str): target output directory path.  If given directory doesn't exist,
     the object will attempt to create it (and all necessary parent directories).
    p_interval (int): interval between two outputs (in seconds)

  Raises:
    XtdError: ``p_directory`` isn't writable or could ne be created
  """
  def __init__(self, p_directory, p_interval = 50):
    super().__init__(__name__ + "." + self.__class__.__name__, p_interval)
    self.m_dir = p_directory
    self._create_dir(self.m_dir)

  @staticmethod
  def _create_dir(p_dir):
    if not os.path.isdir(p_dir):
      try:
        os.makedirs(p_dir, mode=0o0750)
      except Exception as l_error:
        l_fmt = "unable to create output directory '%s' : %s"
        raise XtdError(__name__,  l_fmt % (p_dir, str(l_error)))

  def _write_item(self, p_path, p_name, p_value):
    l_path = os.path.join(self.m_dir, p_path.replace(".", "/"))
    self._create_dir(l_path)
    l_path = os.path.join(l_path, p_name)
    try:
      with open(l_path, mode="w") as l_file:
        l_file.write(str(p_value))
    except Exception as l_error:
      logger.error(self.m_name, "unable to output counter file '%s' : %s", l_path, str(l_error))

  def write(self, p_counters):
    """ Write all available counters to filesystem

    When object fails to write a counte file, an error log is triggered. Raising an
    exception woudn't be helpfull since this part of the code runs in a dedicated
    thread.

    Args:
      p_counters (dict) : see :py:meth:`BaseHandler.write`
    """
    for c_path, c_counter in p_counters.items():
      c_counter.update()
      def visitor(p_name, p_value):
        #pylint: disable=cell-var-from-loop
        self._write_item(c_path, p_name, p_value)
      c_counter.visit(visitor)


#------------------------------------------------------------------#

class HttpHandler(BaseHandler):
  """ Send counter values to a http server

  Counter values are gathered in a single json and sent to
  the target url as a POST request.

  HTTP Request details :

  - Method : ``POST``
  - Content-Type : ``application/json``
  - Body :

    ::

      {
        "namespace-of-counter-1" : value-of-counter-1,
        "namespace-of-counter-2" : value-of-counter-2,
        ...

        "namespace-of-counter-N" : value-of-counter-N
      }


  Note:
    Keep in mind that counter values can be undefined.

    In such case, the json value is a string equals to ``"NaN"``.
  """
  def __init__(self, p_url, p_interval = 50):
    super().__init__(__name__ + "." + self.__class__.__name__, p_interval)
    self.m_url = p_url

  def _send_request(self, p_json):
    try:
      l_headers = { "Content-Type" : "application/json" }
      l_req     = requests.post(self.m_url, headers=l_headers, data=p_json)
      if l_req.status_code != 200:
        l_message = "timeout received invalid http reponse '%d' on posting json"
        logger.error(self.m_name, l_message, l_req.status_code)
    except requests.exceptions.RequestException as l_error:
      logger.error(self.m_name, "error while sending counters data : '%s'", str(l_error))

  def write(self, p_counters):
    """ Write all available counters to filesystem

    When object fails to send HTTP request, an error log is triggered. Raising an
    exception woudn't be helpfull since this part of the code runs in a dedicated
    thread.

    Args:
      p_counters (dict) : see :py:meth:`BaseHandler.write`
    """
    l_res = {}
    for c_path, c_counter in p_counters.items():
      c_counter.update()
      l_item = l_res
      for c_part in c_path.split("."):
        if not c_part in l_item:
          l_item[c_part] = {}
        l_item = l_item[c_part]
      def visitor(p_name, p_value):
        #pylint: disable=cell-var-from-loop
        l_item[p_name] = p_value
      c_counter.visit(visitor)
    self._send_request(l_res)


#------------------------------------------------------------------#

# Local Variables:
# ispell-local-dictionary: "american"
# End:

#  LocalWords:  XtdError
