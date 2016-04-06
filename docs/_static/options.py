import xtd.core.application
import xtd.core.config
import xtd.core.logger
import xtd.core.config.checkers

class MergeApplication(xtd.core.application.Application):
  def __init__(self):
    super().__init__("MergeApplication")

    self.m_config.register_section("input", "Input settings", [{
      "name"        : "directory",
      "default"     : "./work_to_do/",
      "description" : "Read input files from given directory",
      "checks"      : xtd.core.config.checkers.is_dir(p_write=True)
    },{
      "name"        : "count",
      "default"     : 1,
      "description" : "Number of file to read in directory",
      "checks"      : xtd.core.config.checkers.is_int(p_min=0)
    }])

    self.m_config.register_section("output", "Output settings", [{
      "name"        : "file",
      "description" : "Destination file",
      "checks"      : xtd.core.config.checkers.is_file(p_write=True)
    }])


if __name__ == "__main__":
  l_app = MergeApplication()
  l_app.execute()
