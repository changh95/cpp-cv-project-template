#!/usr/bin/env bash
# @file      install_python_packages.sh
# @author    Hyunggi Chang     [github:changh95]
#
# Copyright (c) 2021 Hyunggi Chang, all rights reserved

python3 -m venv python_venv
source python_venv/bin/activate
pip3 install -r ./requirements.txt
deactivate