import xtd.core.application

class MergeApplication(xtd.core.application.Application):
  def __init__(self):
    super().__init__("MyAppName")
    # register input options

  def initialize(self):
    super().initialize()
    # do some initialization suff

  def process(self):
    l_exitCode = 0
    # do some stuff
    return l_exitCode, True

MergeApplication().execute()
