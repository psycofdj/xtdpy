# -*- coding: utf-8
# pylint: disable=unused-import
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

import sys


from .                    import stat, logger, config, param, mixin
from .error.exception     import ConfigException, XtdException

#------------------------------------------------------------------#

class Application(metaclass=mixin.Singleton):
  def __init__(self, p_name = sys.argv[0]):
    self.m_name    = p_name
    self.m_argv    = []
    self.m_config  = config.manager.ConfigManager()
    self.m_signals = []
    self.m_stat    = None
    self.m_param   = None
    self.m_logger  = None

    self.m_config.register_section("general", "General Settings", [{
      "name"        : "config-file",
      "default"     : "%s.json" % self.m_name,
      "description" : "use FILE as configuration file",
      "longopt"     : "--config-file",
      "checks"      : config.checkers.is_file(p_read=True)

    }])

    self.config().register_section("log", "Logging Settings", [{
      "name"        : "level",
      "default"     : "%s.log" % self.m_name,
      "description" : """set logging level to VAL\n
                       * 10 debug\n
                       * 20 info\n
                       * 30 warning\n
                       * 40 error\n
                       * 50 critical\n
      """,
      "checks"      : config.checkers.is_enum(p_values=[10,20,30,40,50])
    },{
      "name"        : "config",
      "default"     : {},
      "description" : "Logging configuration",
      "checks"      : config.checkers.is_json()
    },{
      "name"        : "override",
      "default"     : {},
      "description" : "override part of logging configuration",
      "checks"      : config.checkers.check_json
    }])

    self.config().register_section("stat", "Stats Settings", [{
      "name"        : "writters",
      "default"     : ["disk"],
      "description" : """Enabled given stat output writter. Possibles values :\n
                         * disk : write counters to --stat-disk-directory
                                  path each --stat-disk-interval seconds\n
                         * http : post counters in json format to --stat-http-url
                                  url each --stat-http-interval seconds\n
                         Can specify a comma separated combinaison of theses values\n
      """,
      "checks"      : config.checkers.is_array(
        p_check=config.checkers.is_enum(p_values=["", "disk", "http"])
      )
    },{
      "name"        : "disk-directory",
      "default"     : "/tmp/snmp/%s/stat/" % self.m_name,
      "description" : "Destination directory for counter disk writter"
    },{
      "name"        : "disk-interval",
      "default"     : 50,
      "description" : "Interval in second between two disk outputs",
      "checks"      : config.checkers.is_int()
    },{
      "name"        : "http-url",
      "default"     : "http://localhost/counter",
      "description" : "Destination POST url for http stat writter"
    },{
      "name"        : "http-interval",
      "default"     : 50,
      "description" : "Interval in second between two http outputs",
      "checks"      : config.checkers.is_int()
    }])

    self.config().register_section("param", "Persitent Param Settings", [{
      "name"        : "directory",
      "default"     : "/tmp/snmp/%s/admin" % self.m_name,
      "description" : "Destination directory for admin persistent parameters"
    }])

  def config(self):
    return self.m_config

  # pylint: disable=no-self-use
  def process(self):
    return 0

  def define_counters(self):
    pass

  def _initialize_config(self):
    self.m_config.initialize()
    self.m_config.parse(self.m_argv)

  def _initialize_stat(self):
    self.m_stat = stat.manager.StatManager()
    l_outputters = self.config().get("stat", "writters")
    for c_name in l_outputters:
      if c_name == "disk":
        l_dir      = config.get("stat", "disk-directory")
        l_interval = config.get("stat", "disk-interval")
        l_disk     = stat.writter.DiskWritter(l_dir, l_interval)
        self.m_stat.add_handler(l_disk)
      elif c_name == "http":
        l_url      = config.get("stat", "http-url")
        l_interval = config.get("stat", "http-interval")
        l_http      = stat.writter.HttpWritter(l_url, l_interval)
        self.m_stat.add_handler(l_http)

  def _initialize_log(self):
    self.m_logger = logger.manager.LogManager()
    self.m_logger.initialize(config.get("log", "config"), config.get("log", "override"))

  def _initialize_param(self):
    self.m_param = param.manager.ParamManager(config.get("param", "directory"))

  def initialize(self):
    self._initialize_config()
    self._initialize_log()
    self._initialize_stat()
    self._initialize_param()

  def start(self):
    self.m_stat.start()

  def join(self):
    self.m_stat.join()

  def stop(self):
    self.m_stat.stop()

  def execute(self, p_argv=None):
    if p_argv is None:
      p_argv = sys.argv
    self.m_argv = p_argv

    try:
      self.initialize()
      self.define_counters()
    except ConfigException as l_error:
      print(l_error)
      self.m_config.help()
      sys.exit(1)
    except XtdException as l_error:
      print(l_error)
      sys.exit(1)

    try:
      logger.info(__name__, "starting process")
      self.start()
      l_code = self.process()
      self.join()
      logger.info(__name__, "process finished (status=%d)", l_code)
    except XtdException as l_error:
      logger.exception("core.application", "uncaught exception '%s', exit(1)", l_error)
      sys.exit(1)
