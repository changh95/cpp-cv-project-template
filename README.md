![title](./resource/project_title.png)

> "It's never been easier than this!"

## Purpose :fire:

This repo contains a C++ project template for developing computer vision applications.

## Features :star2:

- The project comprise a widely-used C++ project structure.
- The project supports installing essential toolchains for C++ programming and debugging.
   - git, build-essentials, cppcheck, cmake, clang, gcc, clang-tools, clang-tidy, lldb, lld, libc++, libomp (:heavy_check_mark:)
- The project supports the following 3rdParty libraries:
   - Python3 + basic packages (numpy, pandas, matplotlib, jupyter notebook, voila, tqdm, nbconvert) (:heavy_check_mark:)
   - Open3D (:heavy_check_mark:)
   - Eigen (:heavy_check_mark:)
   - OpenCV (:heavy_check_mark:)
      - Non-free algorithms enabled
   - Ceres-solver (:heavy_check_mark:)
   - GTSAM (:heavy_check_mark:)
   - PCL (:heavy_check_mark:)
      - Visualization disabled
   - OpenGL (:heavy_multiplication_x:)
- The project supports various tools to make good C++ project practices.
   - GTest (:heavy_multiplication_x:)
   - spdlog (:heavy_check_mark:)
   - fast-cpp-csv-parser (:heavy_check_mark:)
   - nlohmann-json (:heavy_check_mark:)

Status legend:
:heavy_check_mark: - Fully supported, 
:white_check_mark: - Partially supported / Build-only, 
:heavy_multiplication_x: - Not supported yet

## How to use :book:

>You need [Python3](https://www.python.org/) to use the automation scripts for project setup and build.

### Linux

```bash
# Install Python 3
sudo apt install python3

# Edit `setup_config.yaml` to configure project
gedit setup_config.yaml

# Install dependencies
chmod u+x setup.py
./setup.py
```

- Edit the [setup_config.yaml](./setup_config.yaml) file to configure your project dependencies.
- You can also use the optional `--password` argument to avoid manually typing your Linux password for every internal sudo command usage.

### Windows

- For now, Windows native build is not supported. Instead, you may use [Windows Subsystems for Linux (WSL)](https://docs.microsoft.com/en-gb/windows/wsl/install-win10) to use the build scripts.

## License :bank:

This repo is licensed under MIT license. Click [here]([./LICENSE](https://github.com/changh95/cpp-cv-project-template/blob/main/LICENSE)) to view the license.

## Contributors :sunglasses:

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
