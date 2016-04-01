#!/usr/bin/env python3
# -*- mode: python -*-

import sys
import re
import subprocess

l_process = subprocess.Popen(["./scripts/lint.sh"], stdout=subprocess.PIPE, shell=True)
l_process.wait()

l_ret   = l_process.returncode
l_lines = l_process.stdout.readlines()
l_line  = l_lines[-2:][0].decode("utf-8")
l_score = re.sub(r"Your code has been rated at ([0-9.]+)/10.*", r"\1", l_line)
l_score = float(l_score.strip())

print("ret code : " + str(l_ret))
if l_ret & 1 or l_ret & 2:
  print("pylint reports unacceptable fatals/errors")
  print(str("status [" + l_line + "]"))
  for c_line in l_lines:
    sys.stdout.write(c_line.decode("utf-8"))
  sys.exit(1)
elif l_ret & 32:
  print("error while running pylint")
  sys.exit(1)
elif l_score < 9.0:
  print("pylint reports unacceptable score of %f" % l_score)
  sys.exit(1)
else:
  print("pylint reports acceptable score of %.2f" % l_score)
  sys.exit(0)

