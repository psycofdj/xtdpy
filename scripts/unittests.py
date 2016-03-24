#!/usr/bin/env python3

import unittest
import importlib
import os
import sys

l_path = os.path.realpath(os.path.dirname(__file__))
os.chdir(os.path.dirname(l_path))
sys.path.append(".")

def list_test():
  l_list = []
  for c_root, c_dirs, c_files in os.walk("xtd/test"):
    l_list += [ os.path.join(c_root,x) for x in c_files if x.startswith("test") and x.endswith(".py") ]
  return l_list

def load_file(p_file):
  l_dir, l_name = os.path.split(p_file)
  l_module  = l_name.split(".")[0]
  l_package = l_dir.replace("/", ".")
  return importlib.import_module("%s.%s" % (l_package, l_module))

def load_tests(p_loader, p_tests, p_patterns):
  l_suite = unittest.TestSuite()
  for c_test in list_test():
    l_module = load_file(c_test)
    l_testsObjs  = []
    for c_item in [ x for x in dir(l_module) if x.endswith("Test") ]:
      l_class = getattr(l_module, c_item)
      l_testCase = p_loader.loadTestsFromTestCase(l_class)
      l_testsObjs += [ l_testCase ]
    l_suite.addTests(l_testsObjs)
  return l_suite

if __name__ == "__main__":
  unittest.main()
