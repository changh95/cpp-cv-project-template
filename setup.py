#!/usr/bin/python3
import argparse
import os
from scripts.third_party_clone.opencv.install_opencv import install_opencv
from scripts.third_party_clone.eigen.install_eigen import install_eigen
from scripts.third_party_clone.ceres.install_ceres_solver import install_ceres_solver


def main():
    parser = argparse.ArgumentParser(description='Script for project setup')
    parser.add_argument('--toolchain', action='store_true',
                        help='Flag for installing essential C++ toolchains: \
                            git, \
                            build-essentials, \
                            cppcheck, \
                            cmake, \
                            clang, \
                            gcc, \
                            clang-tools, \
                            clang-tidy, \
                            lldb, \
                            lld, \
                            libc++, \
                            libomp ')
    parser.add_argument('--opencv', type=str, default="",
                        help='Flag for installing OpenCV of specified version. (e.g. --opencv 4.5.1)')
    parser.add_argument('--opencv_contrib', type=bool, default=False,
                        help='Flag for installing OpenCV_contrib with OpenCV. (True or False)')
    parser.add_argument('--eigen', type=str, default="",
                        help='Flag for installing Eigen of specified version. (e.g. --eigen 3.3.9)')
    parser.add_argument('--ceres', metavar='\b', type=str, default="",
                        help='Flag for installing Ceres-solver of specified version. (e.g. --ceres-solver 2.0.0)')

    args = parser.parse_args()

    if args.toolchain:
        os.system('chmod +x ./scripts/cpp_tool_chains/install_essentials.sh')
        os.system('chmod +x ./scripts/cpp_tool_chains/install_llvm_toolchain.sh')
        os.system('./scripts/cpp_tool_chains/install_essentials.sh')
        os.system('./scripts/cpp_tool_chains/install_llvm_toolchain.sh')

    if args.opencv != "":
        os.system(
            'chmod +x ./scripts/third_party_clone/opencv/install_opencv_deps.sh')
        os.system('./scripts/third_party_clone/opencv/install_opencv_deps.sh')
        installer = install_opencv(args.opencv, args.opencv_contrib)
        installer.run()

    if args.eigen != "":
        installer = install_eigen(args.eigen)
        installer.run()

    if args.ceres != "":
        installer = install_ceres_solver(args.ceres)
        installer.run()

    print("Setup complete!")


if __name__ == '__main__':
    main()
