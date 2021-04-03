#!/usr/bin/python3
import argparse
import os
import sys
from scripts.third_party_clone.opencv.install_opencv import install_opencv
from scripts.third_party_clone.eigen.install_eigen import install_eigen
from scripts.third_party_clone.ceres.install_ceres_solver import install_ceres_solver
from scripts.third_party_clone.gtsam.install_gtsam import install_gtsam


def main():
    parser = argparse.ArgumentParser(description='Script for project setup')
    parser.add_argument('--d', action='store_true',
                        help='Flag for building libraries under debug mode')
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
    parser.add_argument('--opencv', metavar='\b', type=str, default="",
                        help='Flag for installing OpenCV of specified version. (e.g. --opencv 4.5.1)')
    parser.add_argument('--opencv_contrib', action='store_true',
                        help='Flag for installing OpenCV_contrib with OpenCV.')
    parser.add_argument('--eigen', metavar='\b', type=str, default="",
                        help='Flag for installing Eigen of specified version. (e.g. --eigen 3.3.9)')
    parser.add_argument('--ceres', metavar='\b', type=str, default="",
                        help='Flag for installing Ceres-solver of specified version. (e.g. --ceres-solver 2.0.0)')
    parser.add_argument('--gtsam', metavar='\b', type=str, default="",
                        help='Flag for installing GTSAM of specified version. (e.g. --gtsam 4.0.3)')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        return

    if args.toolchain:
        os.system('chmod +x ./scripts/cpp_tool_chains/install_essentials.sh')
        os.system('chmod +x ./scripts/cpp_tool_chains/install_llvm_toolchain.sh')
        os.system('./scripts/cpp_tool_chains/install_essentials.sh')
        os.system('./scripts/cpp_tool_chains/install_llvm_toolchain.sh')

    if args.opencv != "":
        os.system(
            'chmod +x ./scripts/third_party_clone/opencv/install_opencv_deps.sh')
        os.system('./scripts/third_party_clone/opencv/install_opencv_deps.sh')
        installer = install_opencv(args.d, args.opencv, args.opencv_contrib)
        installer.run()

    if args.eigen != "":
        installer = install_eigen(args.d, args.eigen)
        installer.run()

    if args.ceres != "":
        installer = install_ceres_solver(args.d, args.ceres)
        installer.run()

    if args.gtsam != "":
        installer = install_gtsam(args.d, args.gtsam)
        installer.run()

    print("Setup complete!")


if __name__ == '__main__':
    main()
