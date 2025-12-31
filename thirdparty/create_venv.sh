#!/usr/bin/env bash
# @file      install_python_packages.sh
# @author    Hyunggi Chang     [github:changh95]
#
# Copyright (c) 2021 Hyunggi Chang, all rights reserved

python3 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install pipdeptree pip-tools
pip3 install -r ./requirements.txt
deactivate