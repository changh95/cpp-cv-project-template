#!/usr/bin/env python3

import os
import sys
import argparse
import urllib.request
import urllib.error

try:
    __import__("yaml")
except ImportError:
    os.system("pip3 install pyyaml")
import yaml

try:
    __import__("git")
except ImportError:
    os.system("pip3 install gitpython")
import git

pwd = os.path.dirname(os.path.abspath(__file__))


def main():
    # This script installs necessary C++ and Python packages to build and run this program.
    # The package configuration file is read from thirdparty/packages.yaml.

    parser = argparse.ArgumentParser(
        description='Script for project setup. It reads setup configuration from `package.yaml` file.')
    parser.add_argument('--d', action='store_true',
                        help='Enable building libraries in debug mode as well')
    parser.add_argument('--system', action='store_true',
                        help='Install libraries in /usr/local instead of inside the project folder')
    # parser.add_argument('--j', type=int, default=0, help='Number of CPU cores to be used for build')
    parser.add_argument('--password', metavar='\b', type=str, default="",
                        help='Provide your Linux password to avoid manually typing in your password for every auto '
                             'internal \'sudo\' command usage. This will leave traces of your password in your shell '
                             'history. If you are concerned about security, do not use this option.')
    args = parser.parse_args()

    global install_in_system
    install_in_system = False

    #global num_cpus
    #num_cpus = args.j

    if args.system:
        install_in_system = True

    global cfg
    config_file_name = "packages.yaml"
    config_file_path = "./thirdparty/" + config_file_name
    if not os.path.isfile(config_file_path):
        parser.print_help()
        return
    cfg = YAMLparser(config_file_path)

    global base_path
    base_path = os.getcwd()

    global pw
    pw = Password(args.password)

    install_linux_packages()
    install_cpp_packages()
    install_build_packages(args.d)
    install_python_packages()


class Password:
    def __init__(self, password):
        self.data = password

    def sudo(self):
        if self.data == "":
            return "sudo "

        return "echo " + self.data + " | sudo -S "


class YAMLparser:
    def __init__(self, file_path):
        try:
            with open(file_path) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            sys.exit("Error: " + file_path + " not found!")

        for key_L1 in data:  # key_L1 = Level 1 key
            line = data[key_L1]  # Each line in YAML file

            if key_L1 == "apt_packages":
                self.yaml_cpp = line["yaml-cpp"]
                self.doxygen = line["doxygen"]
                self.png = line["PNG"]
                self.tiff = line["TIFF"]
                self.jpeg = line["JPEG"]
                self.zlib = line["ZLIB"]
                self.glut = line["GLUT"]
                self.glew = line["GLEW"]
                self.glfw = line["GLFW"]
                self.glm = line["GLM"]
                self.json = line["JSON"]
                self.gflags = line["gflags"]

            if key_L1 == "build_packages":
                if "Eigen3" not in line:
                    self.eigen = ""
                else:
                    self.eigen = line["Eigen3"]
                if "OpenCV" not in line:
                    self.opencv = ""
                else:
                    self.opencv = line["OpenCV"]
                if "Pangolin" not in line:
                    self.pangolin = ""
                else:
                    self.pangolin = line["Pangolin"]
                if "spdlog" not in line:
                    self.spdlog = ""
                else:
                    self.spdlog = line["spdlog"]
                if "glog" not in line:
                    self.glog = ""
                else:
                    self.glog = line["glog"]
                if "Ceres" not in line:
                    self.ceres = ""
                else:
                    self.ceres = line["Ceres"]
                if "GTSAM" not in line:
                    self.gtsam = ""
                else:
                    self.gtsam = line["GTSAM"]
                if "PCL" not in line:
                    self.pcl = ""
                else:
                    self.pcl = line["PCL"]
                if "GTest" not in line:
                    self.gtest = ""
                else:
                    self.gtest = line["GTest"]
                if "easy-profiler" not in line:
                    self.easy_profiler = ""
                else:
                    self.easy_profiler = line["easy-profiler"]

            if key_L1 == "python3":
                self.evo = line["EVO"]


def install_linux_packages():
    libs_string = "unzip wget curl git build-essential cmake ninja-build gcc clang-format"
    os.system(pw.sudo() + "apt-get -y install " + libs_string)


def install_cpp_packages():
    libs_string = ""
    if cfg.yaml_cpp:
        libs_string += "libyaml-cpp-dev "
    if cfg.doxygen:
        libs_string += "doxygen "
    if cfg.png:
        libs_string += "libpng-dev "
    if cfg.tiff:
        libs_string += "libtiff-dev "
    if cfg.jpeg:
        libs_string += "libjpeg-dev "
    if cfg.zlib:
        libs_string += "zlib1g-dev "
    if cfg.glut:
        libs_string += "freeglut3-dev "
    if cfg.glew:
        libs_string += "libglew-dev "
    if cfg.glfw:
        libs_string += "libglfw3-dev "
    if cfg.glm:
        libs_string += "libglm-dev "
    if cfg.json:
        libs_string += "libjsoncpp-dev "
    if cfg.glog:
        libs_string += "libgoogle-glog-dev "
    if cfg.gflags:
        libs_string += "libgflags-dev "

    os.system(pw.sudo() + "apt-get -y install " + libs_string)


def install_build_packages(enable_debug):
    if cfg.spdlog != "":
        install_spdlog(cfg.spdlog, enable_debug)
    if cfg.gtest != "":
        install_gtest(cfg.gtest, enable_debug)
    if cfg.easy_profiler != "":
        install_easy_profiler(cfg.easy_profiler, enable_debug)
    if cfg.eigen != "":
        install_eigen(cfg.eigen, enable_debug)
    if cfg.pangolin != "":
        install_pangolin(cfg.pangolin, enable_debug)
    if cfg.opencv != "":
        install_opencv(cfg.opencv, enable_debug)
    if cfg.ceres != "":
        install_ceres(cfg.ceres, enable_debug)
    if cfg.gtsam != "":
         install_gtsam(cfg.gtsam, enable_debug)
    if cfg.pcl != "":
         install_pcl(cfg.pcl, enable_debug)


def install_spdlog(cfg, enable_debug):
    # Only build release mode, since most of the time only the fast loggers are desired
    os.chdir(pwd)

    version_num = cfg['version_num']
    debug_build_flags = ""
    release_build_flags = ""

    for flag in cfg['cmake_flags']['debug']:
        debug_build_flags += flag
        debug_build_flags += " "

    for flag in cfg['cmake_flags']['release']:
        release_build_flags += flag
        release_build_flags += " "

    try:
        os.system(pw.sudo() + "rm -rf ./thirdparty/spdlog")

        os.makedirs("./thirdparty/spdlog")
        os.chdir("./thirdparty/spdlog")

        try:
            urllib.request.urlretrieve(
                "https://github.com/gabime/spdlog/archive/refs/tags/v" + version_num + ".zip",
                "./spdlog.zip")
        except urllib.error.HTTPError as e:
            raise Exception("spdlog: cloning failed")

        if os.system("unzip ./spdlog.zip -d .") != 0:
            raise Exception

        os.makedirs("./build/Release", exist_ok=True)
        os.makedirs("./install/Release", exist_ok=True)
        os.chdir("./build/Release")

        exec_string = "cmake ../../spdlog-" + version_num + " -GNinja -DCMAKE_POSITION_INDEPENDENT_CODE=ON "

        if install_in_system:
            if os.system(
                    exec_string + " -DCMAKE_BUILD_TYPE=Release " + release_build_flags) != 0:
                raise Exception("spdlog: cmake configuration failed")
        else:
            if os.system(
                    exec_string + " -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../install/Release " + release_build_flags) != 0:
                raise Exception("spdlog: cmake configuration failed")

        if os.system("ninja") != 0:
            raise Exception("spdlog: ninja failed")

        if os.system(pw.sudo() + "ninja install") != 0:
            raise Exception("spdlog: ninja install failed")

        os.chdir("../../")
        os.system(pw.sudo() + "rm -rf ./build")
        os.system(pw.sudo() + "rm -rf spdlog-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)


def install_pangolin(cfg, enable_debug):
    os.chdir(pwd)

    version_num = str(cfg['version_num'])
    debug_build_flags = ""
    release_build_flags = ""

    for flag in cfg['cmake_flags']['debug']:
        debug_build_flags += flag
        debug_build_flags += " "

    for flag in cfg['cmake_flags']['release']:
        release_build_flags += flag
        release_build_flags += " "

    try:
        os.system(pw.sudo() + "apt-get -y install libglvnd-dev")
        os.system(pw.sudo() + "apt-get -y install libgl1-mesa-dev")
        os.system(pw.sudo() + "apt-get -y install libegl1-mesa-dev")

        os.system(pw.sudo() + "rm -rf ./thirdparty/pangolin")

        os.makedirs("./thirdparty/pangolin")
        os.chdir("./thirdparty/pangolin")

        try:
            urllib.request.urlretrieve(
                "https://github.com/stevenlovegrove/Pangolin/archive/refs/tags/v" + version_num + ".zip",
                "./pangolin.zip")
        except urllib.error.HTTPError as e:
            raise Exception("pangolin: cloning failed")

        if os.system("unzip ./pangolin -d .") != 0:
            raise Exception

        os.makedirs("./build/Release", exist_ok=True)
        os.makedirs("./install/Release", exist_ok=True)
        os.chdir("./build/Release")

        exec_string = "cmake ../../Pangolin-" + version_num + " -GNinja"
        eigen3_path = base_path + "/thirdparty/eigen/install/Release/share/eigen3/cmake"

        if install_in_system:
            if os.system(
                    exec_string + " -DCMAKE_BUILD_TYPE=Release " + release_build_flags) != 0:
                raise Exception("Pangolin: cmake configuration failed")
        else:
            if os.system(
                    exec_string + " -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../install/Release -DCMAKE_PREFIX_PATH=" + eigen3_path + " " + release_build_flags) != 0:
                raise Exception("Pangolin: cmake configuration failed")

        if os.system("ninja") != 0:
            raise Exception("Pangolin: ninja failed")

        if os.system(pw.sudo() + "ninja install") != 0:
            raise Exception("Pangolin: ninja install failed")

        if enable_debug:
            os.chdir("../../")
            os.makedirs("./build/Debug", exist_ok=True)
            os.makedirs("./install/Debug", exist_ok=True)
            os.chdir("./build/Debug")

            if install_in_system:
                if os.system(
                        exec_string + " -DCMAKE_BUILD_TYPE=Debug " + debug_build_flags) != 0:
                    raise Exception("Pangolin: cmake configuration failed")
            else:
                if os.system(
                        exec_string + " -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=../../install/Debug -DCMAKE_PREFIX_PATH=" + eigen3_path + " " + debug_build_flags) != 0:
                    raise Exception("Pangolin: cmake configuration failed")

                if os.system("ninja") != 0:
                    raise Exception("Pangolin: ninja failed")

                if os.system(pw.sudo() + "ninja install") != 0:
                    raise Exception("Pangolin: ninja install failed")

        os.chdir("../../")
        os.system(pw.sudo() + "rm -rf ./build")
        os.system(pw.sudo() + "rm -rf Pangolin-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)


def install_eigen(cfg, enable_debug):
    os.chdir(pwd)

    version_num = cfg['version_num']
    debug_build_flags = ""
    release_build_flags = ""

    for flag in cfg['cmake_flags']['debug']:
        debug_build_flags += flag
        debug_build_flags += " "

    for flag in cfg['cmake_flags']['release']:
        release_build_flags += flag
        release_build_flags += " "

    try:
        os.system(pw.sudo() + "apt-get -y install libblas-dev")
        os.system(pw.sudo() + "apt-get -y install libatlas-base-dev")
        os.system(pw.sudo() + "apt-get -y install liblapack-dev")

        os.system(pw.sudo() + "rm -rf ./thirdparty/eigen")

        os.makedirs("./thirdparty/eigen")
        os.chdir("./thirdparty/eigen")

        try:
            urllib.request.urlretrieve(
                "https://gitlab.com/libeigen/eigen/-/archive/" + version_num + "/eigen-" + version_num + ".zip",
                "./eigen.zip")
        except urllib.error.HTTPError as e:
            raise Exception("Eigen: cloning failed")

        if os.system("unzip ./eigen.zip -d .") != 0:
            raise Exception

        os.makedirs("./build/Release", exist_ok=True)
        os.makedirs("./install/Release", exist_ok=True)
        os.chdir("./build/Release")

        exec_string = "cmake ../../eigen-" + version_num + " -GNinja"

        if install_in_system:
            if os.system(
                    exec_string + " -DCMAKE_BUILD_TYPE=Release " + release_build_flags) != 0:
                raise Exception("Eigen: cmake configuration failed")
        else:
            if os.system(
                    exec_string + " -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../install/Release " + release_build_flags) != 0:
                raise Exception("Eigen: cmake configuration failed")

        if os.system("ninja") != 0:
            raise Exception("Eigen: ninja failed")

        if os.system(pw.sudo() + "ninja install") != 0:
            raise Exception("Eigen: ninja install failed")

        if enable_debug:
            os.chdir("../../")
            os.makedirs("./build/Debug", exist_ok=True)
            os.makedirs("./install/Debug", exist_ok=True)
            os.chdir("./build/Debug")

            if install_in_system:
                if os.system(
                        exec_string + " -DCMAKE_BUILD_TYPE=Debug " + debug_build_flags) != 0:
                    raise Exception("Eigen: cmake configuration failed")
            else:
                if os.system(
                        exec_string + " -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=../../install/Debug " + debug_build_flags) != 0:
                    raise Exception("Eigen: cmake configuration failed")

            if os.system("ninja") != 0:
                raise Exception("Eigen: ninja failed")

            if os.system(pw.sudo() + "ninja install") != 0:
                raise Exception("Eigen: ninja install failed")

        os.chdir("../../")
        os.system(pw.sudo() + "rm -rf ./build")
        os.system(pw.sudo() + "rm -rf eigen-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)


def install_opencv(cfg, enable_debug):
    # TODO(Hyunggi): Check if we need contrib?
    # TODO(Hyunggi): Check whether we use OpenCV 3 or 4.
    os.chdir(pwd)

    version_num = cfg['version_num']
    debug_build_flags = ""
    release_build_flags = ""

    for flag in cfg['cmake_flags']['debug']:
        debug_build_flags += flag
        debug_build_flags += " "

    for flag in cfg['cmake_flags']['release']:
        release_build_flags += flag
        release_build_flags += " "

    try:
        os.system(pw.sudo() + "apt-get -y install ffmpeg")
        os.system(pw.sudo() + "apt-get -y install libgtk2.0-dev")
        os.system(pw.sudo() + "apt-get -y install pkg-config")
        os.system(pw.sudo() + "apt-get -y install libavcodec-dev")
        os.system(pw.sudo() + "apt-get -y install libswscale-dev")
        os.system(pw.sudo() + "apt-get -y install python-dev")
        os.system(pw.sudo() + "apt-get -y install python-numpy")
        os.system(pw.sudo() + "apt-get -y install libtbb2")
        os.system(pw.sudo() + "apt-get -y install libtbb-dev")
        os.system(pw.sudo() + "apt-get -y install libjpeg-dev")
        os.system(pw.sudo() + "apt-get -y install libpng-dev")
        os.system(pw.sudo() + "apt-get -y install libtiff-dev")
        os.system(pw.sudo() + "apt-get -y install libdc1394-22-dev")
        os.system(pw.sudo() + "rm -rf ./thirdparty/opencv")

        os.makedirs("./thirdparty/opencv")
        os.chdir("./thirdparty/opencv")

        try:
            urllib.request.urlretrieve(
                "https://github.com/opencv/opencv/archive/" + version_num + ".zip",
                "./opencv.zip")
        except urllib.error.HTTPError as e:
            raise Exception("OpenCV: cloning failed")

        os.system("unzip ./opencv.zip -d .")

        os.makedirs("./build/Release", exist_ok=True)
        os.makedirs("./install/Release", exist_ok=True)
        os.chdir("./build/Release")

        exec_string = "cmake ../../opencv-" + version_num + " -GNinja"

        if install_in_system:
            if os.system(
                    exec_string + " -DCMAKE_BUILD_TYPE=Release " + release_build_flags) != 0:
                raise Exception("OpenCV: cmake configuration failed")
        else:
            if os.system(
                    exec_string + " -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../install/Release " + release_build_flags) != 0:
                raise Exception("OpenCV: cmake configuration failed")

        if os.system("ninja") != 0:
            raise Exception("OpenCV: ninja failed")

        if os.system(pw.sudo() + "ninja install") != 0:
            raise Exception("OpenCV: ninja install failed")

        if enable_debug:
            os.chdir("../../")
            os.makedirs("./build/Debug", exist_ok=True)
            os.makedirs("./install/Debug", exist_ok=True)
            os.chdir("./build/Debug")

            if install_in_system:
                if os.system(
                        exec_string + " -DCMAKE_BUILD_TYPE=Debug " + debug_build_flags) != 0:
                    raise Exception("OpenCV: cmake configuration failed")
            else:
                if os.system(
                        exec_string + " -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=../../install/Debug " + debug_build_flags) != 0:
                    raise Exception("OpenCV: cmake configuration failed")

            if os.system("ninja") != 0:
                raise Exception("OpenCV: ninja failed")

            if os.system(pw.sudo() + "ninja install") != 0:
                raise Exception("OpenCV: ninja install failed")

        os.chdir("../../")
        os.system(pw.sudo() + "rm -rf ./build")
        os.system(pw.sudo() + "rm -rf opencv-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)


def install_ceres(cfg, enable_debug):
    os.chdir(pwd)

    version_num = cfg['version_num']
    debug_build_flags = ""
    release_build_flags = ""

    for flag in cfg['cmake_flags']['debug']:
        debug_build_flags += flag
        debug_build_flags += " "

    for flag in cfg['cmake_flags']['release']:
        release_build_flags += flag
        release_build_flags += " "

    try:
        os.system(pw.sudo() + "apt-get -y install libgoogle-glog-dev")
        os.system(pw.sudo() + "apt-get -y install libgflags-dev")
        os.system(pw.sudo() + "apt-get -y install libatlas-base-dev")
        os.system(pw.sudo() + "apt-get -y install libsuitesparse-dev")
        os.system(pw.sudo() + "apt-get -y install libpthread-stubs0-dev")

        os.system(pw.sudo() + "rm -rf ./thirdparty/ceres")

        os.makedirs("./thirdparty/ceres")
        os.chdir("./thirdparty/ceres")

        try:
            urllib.request.urlretrieve(
                "https://github.com/ceres-solver/ceres-solver/archive/refs/tags/" + version_num + ".zip",
                "./ceres.zip")
        except urllib.error.HTTPError as e:
            raise Exception("Ceres-solver: cloning failed")

        os.system("unzip ./ceres.zip -d .")

        os.makedirs("./build/Release")
        os.makedirs("./install/Release")
        os.chdir("./build/Release")

        exec_string = "cmake ../../ceres-solver-" + version_num + " -GNinja"
        eigen3_path = base_path + "/thirdparty/eigen/install/Release/share/eigen3/cmake"

        if install_in_system:
            if os.system(
                    exec_string + " -DCMAKE_BUILD_TYPE=Release " + release_build_flags) != 0:
                raise Exception("Ceres-solver: cmake configuration failed")
        else:
            if os.system(
                    exec_string + " -DEigen3_DIR=" + eigen3_path + " -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../install/Release " + release_build_flags) != 0:
                raise Exception("Ceres-solver: cmake configuration failed")

        if os.system("ninja") != 0:
            raise Exception("Ceres-solver: ninja failed")

        # if os.system("ninja test") != 0:
        #     raise Exception("Ceres-solver: ceres-solver unit test failed")

        if os.system(pw.sudo() + "ninja install") != 0:
            raise Exception("Ceres-solver: ninja install failed")

        if enable_debug:
            os.chdir("../../")
            os.makedirs("./build/Debug", exist_ok=True)
            os.makedirs("./install/Debug", exist_ok=True)
            os.chdir("./build/Debug")

            if install_in_system:
                if os.system(
                        exec_string + " -DCMAKE_BUILD_TYPE=Debug " + debug_build_flags) != 0:
                    raise Exception("Ceres-solver: cmake configuration failed")
            else:
                if os.system(
                        exec_string + " -DEigen3_DIR=" + eigen3_path + " -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=../../install/Debug " + debug_build_flags) != 0:
                    raise Exception("Ceres-solver: cmake configuration failed")

            if os.system("ninja") != 0:
                raise Exception("Ceres-solver: ninja failed")

            # if os.system("ninja test") != 0:
            #     raise Exception("Ceres-solver: ceres-solver unit test failed")

            if os.system(pw.sudo() + "ninja install") != 0:
                raise Exception("Ceres-solver: ninja install failed")

        os.chdir("../../")
        os.system(pw.sudo() + "rm -rf ./build")
        os.system(pw.sudo() + "rm -rf ceres-solver-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)


def install_gtsam(cfg, enable_debug):
    os.chdir(pwd)

    version_num = cfg['version_num']
    debug_build_flags = ""
    release_build_flags = ""

    for flag in cfg['cmake_flags']['debug']:
        debug_build_flags += flag
        debug_build_flags += " "

    for flag in cfg['cmake_flags']['release']:
        release_build_flags += flag
        release_build_flags += " "

    try:
        os.system(pw.sudo() + "apt-get -y install libboost-all-dev")
        os.system(pw.sudo() + "rm -rf ./thirdparty/gtsam")

        os.makedirs("./thirdparty/gtsam")
        os.chdir("./thirdparty/gtsam")

        try:
            urllib.request.urlretrieve(
                "https://github.com/borglab/gtsam/archive/refs/tags/" + version_num + ".zip",
                "./gtsam.zip")
        except urllib.error.HTTPError as e:
            raise Exception("GTSAM: cloning failed")

        os.system("unzip ./gtsam.zip -d .")

        os.makedirs("./build/Release")
        os.makedirs("./install/Release")
        os.chdir("./build/Release")

        exec_string = "cmake ../../gtsam-" + version_num + " -GNinja"
        eigen3_include_path = base_path + "/thirdparty/eigen/install/Release/include/eigen3"

        if install_in_system:
            if os.system(
                    exec_string + " -DCMAKE_BUILD_TYPE=Release " + release_build_flags) != 0:
                raise Exception("GTSAM: cmake configuration failed")
        else:
            if os.system(
                    exec_string + " -DGTSAM_USE_SYSTEM_EIGEN=OFF -DEIGEN3_INCLUDE_DIR=" + eigen3_include_path + " -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../install/Release " + release_build_flags) != 0:
                raise Exception("GTSAM: cmake configuration failed")

        if os.system("ninja") != 0:
            raise Exception("GTSAM: ninja failed")

        if os.system(pw.sudo() + "ninja install") != 0:
            raise Exception("GTSAM: ninja install failed")

        if enable_debug:
            os.chdir("../../")
            os.makedirs("./build/Debug", exist_ok=True)
            os.makedirs("./install/Debug", exist_ok=True)
            os.chdir("./build/Debug")

            if install_in_system:
                if os.system(
                        exec_string + " -DCMAKE_BUILD_TYPE=Debug " + debug_build_flags) != 0:
                    raise Exception("GTSAM: cmake configuration failed")
            else:
                if os.system(
                        exec_string + " -DGTSAM_USE_SYSTEM_EIGEN=OFF -DEIGEN3_INCLUDE_DIR=" + eigen3_include_path + " -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=../../install/Debug " + debug_build_flags) != 0:
                    raise Exception("GTSAM: cmake configuration failed")

            if os.system("ninja") != 0:
                raise Exception("GTSAM: ninja failed")

            if os.system(pw.sudo() + "ninja install") != 0:
                raise Exception("GTSAM: ninja install failed")

        os.chdir("../../")
        os.system(pw.sudo() + "rm -rf ./build")
        os.system(pw.sudo() + "rm -rf gtsam-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)


def install_gtest(cfg, enable_debug):
    # Only install release mode, because debug gtest is useless
    os.chdir(pwd)

    version_num = cfg['version_num']
    debug_build_flags = ""
    release_build_flags = ""

    for flag in cfg['cmake_flags']['debug']:
        debug_build_flags += flag
        debug_build_flags += " "

    for flag in cfg['cmake_flags']['release']:
        release_build_flags += flag
        release_build_flags += " "

    try:
        os.system(pw.sudo() + "rm -rf ./thirdparty/gtest")

        os.makedirs("./thirdparty/gtest")
        os.chdir("./thirdparty/gtest")

        try:
            urllib.request.urlretrieve(
                "https://github.com/google/googletest/archive/refs/tags/release-" + version_num + ".zip",
                "./gtest.zip")
        except urllib.error.HTTPError as e:
            raise Exception("GTest: cloning failed")

        os.system("unzip ./gtest.zip -d .")

        os.makedirs("./build/Release", exist_ok=True)
        os.makedirs("./install/Release", exist_ok=True)
        os.chdir("./build/Release")

        exec_string = "cmake ../../googletest-release-" + version_num + " -GNinja"

        if install_in_system:
            if os.system(
                    exec_string + " -DCMAKE_BUILD_TYPE=Release " + release_build_flags) != 0:
                raise Exception("GTest: cmake configuration failed")
        else:
            if os.system(
                    exec_string + " -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../install/Release " + release_build_flags) != 0:
                raise Exception("GTest: cmake configuration failed")

        if os.system("ninja") != 0:
            raise Exception("GTest: ninja failed")
        if os.system("ninja test") != 0:
            raise Exception("GTest: ceres-solver unit test failed")
        if os.system(pw.sudo() + "ninja install") != 0:
            raise Exception("GTest: ninja install failed")

        os.chdir("../../")
        os.system("sudo rm -rf ./build")
        os.system("sudo rm -rf googletest-release-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)


def install_pcl(cfg, enable_debug):
    os.chdir(pwd)

    version_num = cfg['version_num']
    debug_build_flags = ""
    release_build_flags = ""

    for flag in cfg['cmake_flags']['debug']:
        debug_build_flags += flag
        debug_build_flags += " "

    for flag in cfg['cmake_flags']['release']:
        release_build_flags += flag
        release_build_flags += " "

    try:
        os.system(pw.sudo() + "apt-get -y install libboost-all-dev")
        os.system(pw.sudo() + "apt-get -y install libflann-dev")
        os.system(pw.sudo() + "apt-get -y install libglew-dev")

        os.system(pw.sudo() + "rm -rf ./thirdparty/pcl")

        os.makedirs("./thirdparty/pcl")
        os.chdir("./thirdparty/pcl")

        try:
            urllib.request.urlretrieve(
                "https://github.com/PointCloudLibrary/pcl/archive/refs/tags/pcl-" + version_num + ".zip",
                "./pcl.zip")
        except urllib.error.HTTPError as e:
            raise Exception("PCL: cloning failed")

        os.system("unzip ./pcl.zip -d .")

        os.makedirs("./build/Release")
        os.makedirs("./install/Release")
        os.chdir("./build/Release")

        exec_string = "cmake ../../pcl-pcl-" + version_num + " -GNinja"
        eigen3_include_path = base_path + "/thirdparty/eigen/install/Release/include/eigen3"

        if install_in_system:
            if os.system(
                    exec_string + " -DVISUALIZATION=OFF -DCMAKE_BUILD_TYPE=Release " + release_build_flags) != 0:
                raise Exception("PCL: cmake configuration failed")
        else:
            if os.system(
                    exec_string + " -DVISUALIZATION=OFF -DEIGEN_INCLUDE_DIR=" + eigen3_include_path + " -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../install/Release " + release_build_flags) != 0:
                raise Exception("PCL: cmake configuration failed")

        if os.system("ninja") != 0:
            raise Exception("PCL: ninja failed")

        if os.system(pw.sudo() + "ninja install") != 0:
            raise Exception("PCL: ninja install failed")

        if enable_debug:
            os.chdir("../../")
            os.makedirs("./build/Debug", exist_ok=True)
            os.makedirs("./install/Debug", exist_ok=True)
            os.chdir("./build/Debug")

            if install_in_system:
                if os.system(
                        exec_string + " -DVISUALIZATION=OFF -DCMAKE_BUILD_TYPE=Debug " + debug_build_flags) != 0:
                    raise Exception("PCL: cmake configuration failed")
            else:
                if os.system(
                        exec_string + " -DVISUALIZATION=OFF -DEIGEN_INCLUDE_DIR=" + eigen3_include_path + " -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=../../install/Debug " + debug_build_flags) != 0:
                    raise Exception("PCL: cmake configuration failed")

            if os.system("ninja") != 0:
                raise Exception("PCL: ninja failed")

            if os.system(pw.sudo() + "ninja install") != 0:
                raise Exception("PCL: ninja install failed")

        os.chdir("../../")
        os.system(pw.sudo() + "rm -rf ./build")
        os.system(pw.sudo() + "rm -rf pcl-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)


def install_easy_profiler(cfg, enable_debug):
    # Only install Release version (Debug profiler is too slow!)

    os.chdir(pwd)

    version_num = cfg['version_num']
    debug_build_flags = ""
    release_build_flags = ""

    for flag in cfg['cmake_flags']['debug']:
        debug_build_flags += flag
        debug_build_flags += " "

    for flag in cfg['cmake_flags']['release']:
        release_build_flags += flag
        release_build_flags += " "

    try:
        os.system(pw.sudo() + "apt-get -y install qt5-default libqt5widgets5")
        os.system(pw.sudo() + "rm -rf ./thirdparty/easy_profiler")

        os.makedirs("./thirdparty/easy_profiler")
        os.chdir("./thirdparty/easy_profiler")

        try:
            urllib.request.urlretrieve(
                "https://github.com/yse/easy_profiler/archive/refs/tags/v" + version_num + ".zip",
                "./easy_profiler.zip")
        except urllib.error.HTTPError as e:
            raise Exception("Easy-profiler: cloning failed")

        os.system("unzip ./easy_profiler.zip -d .")

        os.makedirs("./build/Release", exist_ok=True)
        os.makedirs("./install/Release", exist_ok=True)
        os.chdir("./build/Release")

        exec_string = "cmake ../../easy_profiler-" + version_num + " -GNinja"

        if install_in_system:
            if os.system(
                    exec_string + " -DCMAKE_BUILD_TYPE=Release " + release_build_flags) != 0:
                raise Exception("Easy-profiler: cmake configuration failed")
        else:
            if os.system(
                    exec_string + " -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../install/Release " + release_build_flags) != 0:
                raise Exception("Easy-profiler: cmake configuration failed")

        if os.system("ninja") != 0:
            raise Exception("Easy-profiler: ninja failed")

        if os.system(pw.sudo() + "ninja install") != 0:
            raise Exception("Easy-profiler: ninja install failed")

        if not install_in_system:
            # Copy lib files to system
            os.chdir("../../install/Release/lib")
            os.system(pw.sudo() +
                      "cp libeasy_profiler.so /usr/lib/x86_64-linux-gnu/libeasy_profiler.so")

        os.chdir("../../../")
        os.system(pw.sudo() + "rm -rf ./build")
        os.system(pw.sudo() + "rm -rf easy_profiler-" + version_num)

    except Exception as e:
        print("")
        sys.exit(e)


def install_python_packages():
    os.chdir(pwd)

    # Install virtual environment
    os.system(pw.sudo() + "apt-get -y install python3-venv")

    # Installs easydict, numpy, scipy in a virtual environment (.venv)
    os.system("chmod u+x ./thirdparty/create_venv.sh")
    os.system("./thirdparty/create_venv.sh")

    if cfg.evo != "":
        install_evo(cfg.evo)


def install_evo(version_num):
    os.chdir(pwd)

    # install EVO for map evaluation
    try:
        os.system(pw.sudo() + "rm -rf ./thirdparty/evo")
        os.chdir("./thirdparty")

        try:
            urllib.request.urlretrieve(
                "https://github.com/MichaelGrupp/evo/archive/refs/tags/v" + version_num + ".zip",
                "./evo.zip")
        except urllib.error.HTTPError as e:
            raise Exception("EVO: cloning failed")

        os.system("unzip ./evo.zip -d .")
        os.rename("evo-" + version_num, "evo")
        os.system(pw.sudo() + "rm -rf ./evo.zip")

    except Exception as e:
        print("")
        sys.exit(e)

    os.chdir(pwd)
    os.system("chmod u+x ./thirdparty/install_evo.sh")
    os.system("./thirdparty/install_evo.sh")


if __name__ == "__main__":
    main()
