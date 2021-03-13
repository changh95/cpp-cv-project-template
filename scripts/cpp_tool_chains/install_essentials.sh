#!/usr/bin/env bash
# @file      install_cpp_essentials.sh
# @author    Hyunggi Chang     [github:changh95]
#
# Copyright (c) 2021 Hyunggi Chang, all rights reserved

# Remove all existing alternatives
sudo update-alternatives --remove-all cc
sudo update-alternatives --remove-all c++
sudo update-alternatives --remove-all ld
sudo update-alternatives --remove-all clang
sudo update-alternatives --remove-all gcc

# exit on first error
set -e

# Install git, build-essential, cmake, cppcheck
sudo apt install git
sudo apt install build-essential
sudo apt install cmake
sudo apt install cppcheck
