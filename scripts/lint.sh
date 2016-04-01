#!/bin/bash

l_path=$(readlink -f $0)
l_root=$(dirname $(dirname ${l_path}))
cd ${l_root}

l_mode=$1; shift
if [ -z "${l_mode}" ]; then
  l_mode="text"
fi

if [ "${l_mode}" == "html" ]; then
  mkdir -p build/lint
  pylint --rcfile=.pylintrc -j4 --init-hook="import sys; sys.path.append('${l_root}')" -f ${l_mode} xtd $@ > build/lint/index.html
else
  pylint --rcfile=.pylintrc -j4 --init-hook="import sys; sys.path.append('${l_root}')" -f ${l_mode} xtd $@
fi
