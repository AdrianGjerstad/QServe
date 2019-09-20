#!/usr/bin/bash

function qs() {
  if [[ $QSERVE_PATH == "" ]]; then
    QSERVE_PATH="${PWD}/"
    export QSERVE_PATH
  fi

  command -v python3 >/dev/null 2>&1 || { echo "Please install Python3 and try again."; return 1; };

  # Python is in fact installed, run qserve
  python3 ${QSERVE_PATH}qserve.py $@
  echo "Stopped."

  return 0
}