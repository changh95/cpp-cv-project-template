#!/usr/bin/python3
import argparse
import os
from scripts.third_party_clone.opencv.install_opencv import install_opencv


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
                        help='Flag for installing OpenCV of specified version. (e.g. --opencv 4.4.0')
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
        opencv_install = install_opencv(args.opencv)
        opencv_install.run()

    print("Setup complete!")


if __name__ == '__main__':
    main()
