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
./setup.py --toolchain --opencv 4.5.1 --opencv_contrib --eigen 3.3.9 --ceres 2.0.0 --gtsam 4.0.3 --python3 --open3d

```

### Windows - How to use

Download the latest [Python3](https://www.python.org/downloads/windows/).

For now, it is highly recommended to use [Windows Subsystems for Linux (WSL)](https://docs.microsoft.com/en-gb/windows/wsl/install-win10) to use the build scripts. Hopefully I can make build scripts for Windows soon enough...

## Features

- The project comprise a widely-used C++ project structure.
- The project supports installing essential toolchains for C++ programming and debugging.
   - git, build-essentials, cppcheck, cmake, clang, gcc, clang-tools, clang-tidy, lldb, lld, libc++, libomp (:heavy_check_mark:)
- The project supports the following 3rdParty libraries:
   - Python3 + Numpy + matplotlib (:heavy_check_mark:)
   - Open3D (:heavy_check_mark:)
   - Eigen (:white_check_mark:)
   - OpenCV (:white_check_mark:)
      - Non-free algorithms enabled
   - Ceres-solver (:white_check_mark:)
   - GTSAM (:white_check_mark:)
   - PCL (:white_check_mark:)
      - Visualization disabled
   - OpenGL (:heavy_multiplication_x:)
   - GTest (:heavy_multiplication_x:)
   - spdlog (:white_check_mark:)
   - fast-cpp-csv-parser (:white_check_mark:)

Status legend:
:heavy_check_mark: - Fully supported, 
:white_check_mark: - Partially supported / Build-only, 
:heavy_multiplication_x: - Not supported yet
