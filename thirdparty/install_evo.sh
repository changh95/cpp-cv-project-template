#!/bin/bash

function log { echo -e "\033[0;32m[$BASH_SOURCE] $1\033[0m"; }
function echo_and_run { echo -e "\033[0;35m\$ $@\033[0m"; "$@"; }

echo_and_run source .venv/bin/activate
echo_and_run cd ./thirdparty/evo
echo_and_run pip3 install --editable . --upgrade --no-binary evo
echo_and_run cd -
log "------< EVO installation done > ------"
