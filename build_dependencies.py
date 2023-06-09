#!/usr/bin/env python3

import os
import sys
import argparse
import platform
from scripts import install
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
    """
    This script installs necessary C++ and Python packages to build and run this program. 
    The package configuration file is read from thirdparty/packages.yaml.
    """

    parser = argparse.ArgumentParser(
        description='Script for project setup. It reads setup configuration from `package.yaml` file.')
    parser.add_argument('--d', action='store_true',
                        help='Enable building libraries in debug mode as well')
    parser.add_argument('--system', action='store_true',
                        help='Install libraries in /usr/local instead of inside the project folder')
    parser.add_argument('--j', type=int, default=0, help='Number of CPU cores to be used for build')
    parser.add_argument('--password', metavar='\b', type=str, default="",
                        help='Provide your Linux password to avoid manually typing in your password for every auto '
                             'internal \'sudo\' command usage. This will leave traces of your password in your shell '
                             'history. If you are concerned about security, do not use this option.')
    args = parser.parse_args()

    config_file_path = "./thirdparty/packages.yaml"
    if not os.path.isfile(config_file_path):
        parser.print_help()
        return
    
    cfg = Config(config_file_path)
    cfg.basic_config.os_name = platform.system()
    cfg.basic_config.pw = Password(args.password)
    cfg.basic_config.base_path = pwd
    if args.system:
        cfg.basic_config.install_in_system = True
    if args.d:
        cfg.basic_config.d = True
    if args.j != 0:
        cfg.basic_config.nproc = " -j" + str(args.j)

    #install_apt_packages(cfg)
    #install_libraries_from_source(cfg)
    install_python_packages(cfg)


class Password:
    def __init__(self, password):
        self.data = password

    def sudo(self):
        if self.data == "":
            return "sudo "

        return "echo " + self.data + " | sudo -S "


class Config:
    class BasicConfig:
        def __init__(self):
            self.os_name = ""
            self.install_in_system = False
            self.nproc = ""
            self.base_path = ""
            self.pw = Password("")
            self.d = False
    
    def __init__(self, file_path):
        # Basic configs        
        self.basic_config = self.BasicConfig()
                
        # Installation configs 
        try:
            with open(file_path) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            sys.exit("Error: " + file_path + " not found!")

        # Initialize the attributes to empty strings
        self.eigen = ""
        self.opencv = ""
        self.pangolin = ""
        self.spdlog = ""
        self.glog = ""
        self.ceres = ""
        self.gtsam = ""
        self.pcl = ""
        self.gtest = ""
        self.easy_profiler = ""
        self.evo = ""
        self.boost = ""
        self.yaml_cpp = ""
        self.doxygen = ""
        self.png = ""
        self.tiff = ""
        self.jpeg = ""
        self.zlib = ""
        self.glut = ""
        self.glew = ""
        self.glfw = ""
        self.glm = ""
        self.json = ""
        self.gflags = ""

        for key_L1 in data:  # key_L1 = Level 1 key
            line = data[key_L1]  # Each line in YAML file

            if key_L1 == "apt_packages":
                self.yaml_cpp = line.get("yaml-cpp", "")
                self.doxygen = line.get("doxygen", "")
                self.png = line.get("PNG", "")
                self.tiff = line.get("TIFF", "")
                self.jpeg = line.get("JPEG", "")
                self.zlib = line.get("ZLIB", "")
                self.glut = line.get("GLUT", "")
                self.glew = line.get("GLEW", "")
                self.glfw = line.get("GLFW", "")
                self.glm = line.get("GLM", "")
                self.json = line.get("JSON", "")
                self.gflags = line.get("gflags", "")

            if key_L1 == "build_packages":
                self.eigen = line.get("Eigen3", "")
                self.opencv = line.get("OpenCV", "")
                self.pangolin = line.get("Pangolin", "")
                self.spdlog = line.get("spdlog", "")
                self.glog = line.get("glog", "")
                self.ceres = line.get("Ceres", "")
                self.gtsam = line.get("GTSAM", "")
                self.pcl = line.get("PCL", "")
                self.gtest = line.get("GTest", "")
                self.easy_profiler = line.get("easy-profiler", "")

            if key_L1 == "python3":
                self.evo = line.get("EVO", "")


def install_apt_packages(cfg):
    install.install_apt_essential(cfg)
    install.install_apt_optional(cfg)


def install_libraries_from_source(cfg):
    if cfg.spdlog != "":
        install.build_and_install_spdlog(cfg.spdlog, cfg.basic_config)
    if cfg.gtest != "":
       install.build_and_install_gtest(cfg.gtest, cfg.basic_config)
    if cfg.easy_profiler != "":
       install.build_and_install_easy_profiler(cfg.easy_profiler, cfg.basic_config)
    if cfg.eigen != "":
       install.build_and_install_eigen(cfg.eigen, cfg.basic_config)
    if cfg.pangolin != "":
       install.build_and_install_pangolin(cfg.pangolin, cfg.basic_config)
    if cfg.opencv != "":
       install.build_and_install_opencv(cfg.opencv, cfg.basic_config)
    if cfg.ceres != "":
       install.build_and_install_ceres(cfg.ceres, cfg.basic_config)
    if cfg.gtsam != "":
       install.build_and_install_gtsam(cfg.gtsam, cfg.basic_config)
    if cfg.pcl != "":
       install.build_and_install_pcl(cfg.pcl, cfg.basic_config)

def install_python_packages(cfg):
    install.create_venv(cfg)
    
    if cfg.evo != "":
        install.install_evo(cfg)


if __name__ == "__main__":
    main()
