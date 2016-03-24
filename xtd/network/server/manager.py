# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"
__version__   = "0.3"

#------------------------------------------------------------------#

import urllib
import re
import cherrypy
import logging

from xtd.core      import logger
from xtd.core.stat import counter
from .             import tools

#------------------------------------------------------------------#

class ServerManager:
  ms_initialized = False
  ms_perfCounter = None

  class LoggerFilter(logging.Filter):
    def __init__(self, p_name=""):
      super().__init__(p_name)


    def filter(self, p_record):
      l_logger = logger.get(self.name)
      p_record.msg  = re.sub("^\[[^\]]*\] *", "", p_record.msg)
      p_record.msg  = re.sub("^ENGINE *", "",     p_record.msg)
      p_record.name = self.name
      l_logger.handle(p_record)
      return None

  @classmethod
  def listen(p_class, p_socket, p_nbThreads = 10, p_tls = False, p_cacert = None, p_cert = None, p_key = None):
    if not p_class.ms_initialized:
      raise BaseException(__name__, "you must initialize server manager first")
    l_server = cherrypy._cpserver.Server()
    p_socket = urllib.parse.urlparse(p_socket)
    if p_socket.scheme == "tcp":
      l_server.socket_host = p_socket.hostname
      l_port = p_socket.port
      if not l_port:
        l_port = 8080
      l_server.socket_port = l_port
    elif p_socket.scheme == "unix":
      l_server.bind_addr = p_socket.path
    l_server.thread_pool           = p_nbThreads
    if p_tls:
      cherrypy.log("Enabling TLS support")
      l_server.ssl_module            = "builtin"
      #l_server.ssl_certificate_chain = p_cacert
      l_server.ssl_certificate       = p_cert
      l_server.ssl_private_key       = p_key
    l_server.subscribe()
    return l_server

  @classmethod
  def get_counter(p_class):
    return p_class.ms_counter

  @classmethod
  def initialize(p_class, p_logger):
    if p_class.ms_initialized:
      return None
    p_class.ms_counter = counter.AvgTimePerf("rtt")

    cherrypy.tools.counter_start        = cherrypy._cptools.Tool("on_start_resource", p_class.ms_counter.work_begin)
    cherrypy.tools.counter_stop         = cherrypy._cptools.Tool("on_end_request",    p_class.ms_counter.work_end)
    cherrypy.tools.log_request          = cherrypy._cptools.Tool('on_start_resource', tools.request_logger("debug", p_logger + ".request"))
    cherrypy.tools.log_response         = cherrypy._cptools.Tool('on_end_resource',   tools.response_logger("debug", p_logger + ".response"))

    cherrypy.server.unsubscribe()
    l_filterAccess = p_class.LoggerFilter(p_logger + ".access")
    l_filterError  = p_class.LoggerFilter(p_logger + ".error")
    logging.getLogger("cherrypy.acccess").addFilter(l_filterAccess)
    logging.getLogger("cherrypy.error").addFilter(l_filterError)
    cherrypy.config.update({
      "environment"                   : "production",
      "engine.autoreload.on"          : False,
      "log.screen"                    : True,
      "log.access_file"               : "",
      "log.error_file"                : "",
      "tools.counter_start.on"        : True,
      "tools.counter_stop.on"         : True,
      "tools.log_request.on"          : True,
      "tools.log_response.on"         : True
    })
    cherrypy.engine.signals.subscribe()
    p_class.ms_initialized = True

  @classmethod
  def mount(p_class, p_handler, p_path, p_conf = {}, p_logger = "cherrypy"):
    if not p_class.ms_initialized:
      raise BaseException(__name__, "you must initialize server manager first")
    l_app = cherrypy.tree.mount(p_handler, p_path, p_conf)
    l_app.log.error_log = logging.getLogger(p_logger + ".error")
    l_app.log.access_log = logging.getLogger(p_logger + ".access")

  @classmethod
  def subscribe(p_class, p_channel, p_handler, p_prio):
    if not p_class.ms_initialized:
      raise BaseException(__name__, "you must initialize server manager first")
    cherrypy.engine.subscribe(p_channel, p_handler, p_prio)

  @classmethod

  def start(p_class):
    if not p_class.ms_initialized:
      raise BaseException(__name__, "you must initialize server manager first")
    cherrypy.engine.start()

  @classmethod
  def join(p_class):
    if not p_class.ms_initialized:
      raise BaseException(__name__, "you must initialize server manager first")
    cherrypy.engine.block()

  @classmethod
  def stop(p_class):
    if not p_class.ms_initialized:
      raise BaseException(__name__, "you must initialize server manager first")
    cherrypy.engine.stop();
