# cpp-cv-project-template

## Purpose

This repo contains a C++ project template for developing computer vision applications.

## Dependencies

You need [Python3](https://www.python.org/) to use the automation scripts for project setup and build.

### Linux - How to use

```bash
# Install Python 3
sudo apt install python3

# Project setup - Install dependencies
chmod u+x setup.py
./setup.py --toolchain --opencv 4.5.1 --opencv_contrib --eigen 3.3.9 --ceres 2.0.0 --gtsam 4.0.3

```

### Windows - How to use

Download the latest [Python3](https://www.python.org/downloads/windows/).

For now, it is highly recommended to use [Windows Subsystems for Linux (WSL)](https://docs.microsoft.com/en-gb/windows/wsl/install-win10) to use the build scripts. Hopefully I can make build scripts for Windows soon enough...

## Features

- The project comprise a widely-used C++ project structure.
- The project supports installing essential toolchains for C++ programming and debugging.
   - git, build-essentials, cppcheck, cmake, clang, gcc, clang-tools, clang-tidy, lldb, lld, libc++, libomp
- The project supports the following 3rdParty libraries:
   - Eigen (On-going)
   - OpenCV (On-going)
   - GTest (TODO)
   - Ceres-solver (On-going)
   - GTSAM (On-going)
   - OpenGL (TODO)
   - fast-cpp-csv-parser (TODO)

