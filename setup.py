#!/usr/bin/python3
import argparse
import os
import sys
import shutil
from scripts.third_party_clone.cpp_utils import install_cpp_utils
from scripts.third_party_clone.opencv.install_opencv import install_opencv
from scripts.third_party_clone.eigen.install_eigen import install_eigen
from scripts.third_party_clone.ceres.install_ceres_solver import install_ceres_solver
from scripts.third_party_clone.gtsam.install_gtsam import install_gtsam
from scripts.third_party_clone.pcl.install_pcl import install_pcl

class Password:
    def __init__(self):
        self.exist = False
        self.data = ""

    def fill(self, password):
        self.exist = True
        self.data = password

    def redeem(self):
        if self.data == "":
            return

        execString = "echo \"" + self.data + "\" | sudo -S echo \"Password activated\""
        os.system(execString)


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
    parser.add_argument('--utils', action='store_true',
                        help='Flag for installing C++ utilities: \
                            spdlog, \
                            fast-cpp-csv-parser')
    parser.add_argument('--opencv', metavar='\b', type=str, default="",
                        help='Flag for installing OpenCV of specified version. (e.g. --opencv 4.5.1)')
    parser.add_argument('--opencv_contrib', action='store_true',
                        help='Flag for installing OpenCV_contrib with OpenCV.')
    parser.add_argument('--eigen', metavar='\b', type=str, default="",
                        help='Flag for installing Eigen of specified version. (e.g. --eigen 3.3.9)')
    parser.add_argument('--pcl', metavar='\b', type=str, default="",
                        help='Flag for installing PCL of specified version. (e.g. --pcl 1.11.1)')
    parser.add_argument('--ceres', metavar='\b', type=str, default="",
                        help='Flag for installing Ceres-solver of specified version. (e.g. --ceres 2.0.0)')
    parser.add_argument('--gtsam', metavar='\b', type=str, default="",
                        help='Flag for installing GTSAM of specified version. (e.g. --gtsam 4.0.3)')
    parser.add_argument('--python3', action='store_true',
                        help='Flag for installing Python3 and some useful tools. By default, numpy, pandas, matplotlib, jupyter notebook, voila, tqdm, nbconvert are installed')
    parser.add_argument('--open3d', action='store_true',
                        help='Flag for installing Open3D Python library. Numpy, Scikit-Learn, Pandas, Pillow, matplotlib are automatically installed')
    parser.add_argument('--opencv_python', action='store_true',
                        help='Flag for installing OpenCV-python library.')
    parser.add_argument('--opencv_contrib_python', action='store_true',
                        help='Flag for installing opencv_contrib for python. `--opencv_python` flag needs to be set.')
    parser.add_argument('--password', metavar='\b', type=str, default="",
    help='Provide your Linux password to avoid manually typing in your password for every auto internal \'sudo\' command usage. This will leave traces of your password in your shell history - if you are concerned about security, do not use this option.')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        return

    status_str = "Setup complete!: "

    pw = Password()
    if args.password != "":
        pw.fill(args.password)

    if args.toolchain:
        pw.redeem()
        os.system('chmod +x ./scripts/cpp_tool_chains/install_essentials.sh')
        os.system('chmod +x ./scripts/cpp_tool_chains/install_llvm_toolchain.sh')
        os.system('./scripts/cpp_tool_chains/install_essentials.sh')
        os.system('./scripts/cpp_tool_chains/install_llvm_toolchain.sh')
        status_str += "--toolchain, "

    if args.utils:
        installer = install_cpp_utils(args.d, pw)
        installer.run()
        status_str += "--utils, "

    if args.opencv != "":
        pw.redeem()
        os.system(
            'chmod +x ./scripts/third_party_clone/opencv/install_opencv_deps.sh')
        os.system('./scripts/third_party_clone/opencv/install_opencv_deps.sh')
        installer = install_opencv(args.d, args.opencv, args.opencv_contrib, pw)
        installer.run()
        status_str += "--opencv, "

        if args.opencv_contrib:
            status_str += "--opencv_contrib, "

    if args.eigen != "":
        installer = install_eigen(args.d, args.eigen, pw)
        installer.run()
        status_str += "--eigen, "

    if args.pcl != "":
        if args.eigen == "":
            installer = install_eigen(args.d, "3.3.9", pw)
            installer.run()

        installer = install_pcl(args.d, args.pcl, pw)
        installer.run()
        status_str += "--pcl, "

    if args.ceres != "":
        if args.eigen == "":
            installer = install_eigen(args.d, "3.3.9", pw)
            installer.run()

        installer = install_ceres_solver(args.d, args.ceres, pw)
        installer.run()
        status_str += "--ceres, "

    if args.gtsam != "":
        installer = install_gtsam(args.d, args.gtsam, pw)
        installer.run()
        status_str += "--gtsam, "

    if args.python3 or args.open3d or args.opencv_python:
        pw.redeem()

        os.system('sudo apt install -y python3 python3-venv')
        shutil.rmtree('./python_venv', ignore_errors=True)
        os.system('> requirements.txt')

        if args.python3:
            os.system('cat ./scripts/python_packages/basic_python_packages.txt >> ./requirements.txt')
            status_str += "--python3, "

        if args.open3d:
            os.system('cat ./scripts/python_packages/open3d.txt >> ./requirements.txt')
            status_str += "--open3d, "

        if args.opencv_python:
            os.system('cat ./scripts/python_packages/opencv-python.txt >> ./requirements.txt')
            status_str += "--opencv_python, "

            if args.opencv_contrib_python:
                os.system('cat ./scripts/python_packages/opencv-contrib-python.txt >> ./requirements.txt')
                status_str += "--opencv_contrib_python, "

        os.system('chmod u+x ./scripts/python_packages/install_python_packages.sh')
        os.system('./scripts/python_packages/install_python_packages.sh')

    print(status_str)


if __name__ == '__main__':
    main()
