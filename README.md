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
./setup.py --toolchain --utils --opencv 4.5.1 --opencv_contrib --eigen 3.3.9 --pcl 1.11.1 --ceres 2.0.0 --gtsam 4.0.3 --python3 --open3d

```

### Windows - How to use

Download the latest [Python3](https://www.python.org/downloads/windows/).

For now, it is highly recommended to use [Windows Subsystems for Linux (WSL)](https://docs.microsoft.com/en-gb/windows/wsl/install-win10) to use the build scripts. Hopefully I can make build scripts for Windows soon enough...

## Features

- The project comprise a widely-used C++ project structure.
- The project supports installing essential toolchains for C++ programming and debugging.
   - git, build-essentials, cppcheck, cmake, clang, gcc, clang-tools, clang-tidy, lldb, lld, libc++, libomp (:heavy_check_mark:)
- The project supports the following 3rdParty libraries:
   - Python3 + basic packages (numpy, pandas, matplotlib, jupyter notebook, voila, tqdm, nbconvert) (:heavy_check_mark:)
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

## License

This repo is licensed under MIT license. Click [here]([./LICENSE](https://github.com/changh95/cpp-cv-project-template/blob/main/LICENSE)) to view the license.

## Contributors

Thanks goes to these wonderful people!

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/changh95"><img src="https://avatars.githubusercontent.com/u/39010111?v=4" width="100px;" alt=""/><br /><sub><b>changh95</b></sub></a><br /><a href="https://github.com/changh95/cpp-cv-project-template/commits?author=changh95" title="Commits">💻</a></td>
    <td align="center"><a href="https://github.com/pacientes"><img src="https://avatars.githubusercontent.com/u/22834091?v=4" width="100px;" alt=""/><br /><sub><b>pacientes</b></sub></a><br /><a href="https://github.com/changh95/cpp-cv-project-template/commits?author=pacientes" title="Commits">💻</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
