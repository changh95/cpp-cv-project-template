#!/usr/bin/python3
import yaml
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

class YAMLparser:
    def __init__(self, file_path):
        try:
            with open(file_path) as f:        
                data = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            sys.exit("Error: " + file_path + " not found!")

        for key_L1 in data: # key_L1 = Level 1 key
            line = data[key_L1] # Each line in YAML file

            if key_L1 == "compile-options":
                self.build_debug = line["build-debug"]
            
            if key_L1 == "library-cpp":
                self.toolchain = line["toolchain"]
                self.utility = line["utility"]
                self.opencv = line["opencv"]
                self.opencv_contrib = line["opencv-contrib"]
                self.eigen = line["eigen"]
                self.pcl = line["pcl"]
                self.ceres = line["ceres"]
                self.gtsam = line["gtsam"]

            if key_L1 == "library-python":
                self.python3 = line["python3"]
                self.open3d = line["open3d"]
                self.opencv_python = line["opencv-python"]
                self.opencv_contrib_python = line["opencv-contrib-python"]


def main():
    parser = argparse.ArgumentParser(description='Script for project setup. It reads setup configuration from `setup_config.yaml` file.')
    parser.add_argument('--password', metavar='\b', type=str, default="",
    help='Provide your Linux password to avoid manually typing in your password for every auto internal \'sudo\' command usage. This will leave traces of your password in your shell history. If you are concerned about security, do not use this option.')

    args = parser.parse_args()

    config_file_path = "./setup_config.yaml"

    if not os.path.isfile(config_file_path):
        parser.print_help()
        return

    cfg = YAMLparser(config_file_path)

    status_str = "Setup complete!: "

    pw = Password()
    if args.password != "":
        pw.fill(args.password)

    if cfg.toolchain:
        pw.redeem()
        os.system('chmod +x ./scripts/cpp_tool_chains/install_essentials.sh')
        os.system('chmod +x ./scripts/cpp_tool_chains/install_llvm_toolchain.sh')
        os.system('./scripts/cpp_tool_chains/install_essentials.sh')
        os.system('./scripts/cpp_tool_chains/install_llvm_toolchain.sh')
        status_str += "--toolchain, "

    if cfg.utility:
        installer = install_cpp_utils(cfg.build_debug, pw)
        installer.run()
        status_str += "--utils, "

    if cfg.opencv != "":
        pw.redeem()
        os.system(
            'chmod +x ./scripts/third_party_clone/opencv/install_opencv_deps.sh')
        os.system('./scripts/third_party_clone/opencv/install_opencv_deps.sh')
        installer = install_opencv(cfg.build_debug, cfg.opencv, cfg.opencv_contrib, pw)
        installer.run()
        status_str += "--opencv, "

        if cfg.opencv_contrib:
            status_str += "--opencv_contrib, "

    if cfg.eigen != "":
        installer = install_eigen(cfg.build_debug, cfg.eigen, pw)
        installer.run()
        status_str += "--eigen, "

    if cfg.pcl != "":
        if cfg.eigen == "":
            installer = install_eigen(cfg.build_debug, "3.3.9", pw)
            installer.run()

        installer = install_pcl(cfg.build_debug, cfg.pcl, pw)
        installer.run()
        status_str += "--pcl, "

    if cfg.ceres != "":
        if cfg.eigen == "":
            installer = install_eigen(cfg.build_debug, "3.3.9", pw)
            installer.run()

        installer = install_ceres_solver(cfg.build_debug, cfg.ceres, pw)
        installer.run()
        status_str += "--ceres, "

    if cfg.gtsam != "":
        installer = install_gtsam(cfg.build_debug, cfg.gtsam, pw)
        installer.run()
        status_str += "--gtsam, "

    if cfg.python3 or cfg.open3d or cfg.opencv_python:
        pw.redeem()

        os.system('sudo apt install -y python3 python3-venv')
        shutil.rmtree('./python_venv', ignore_errors=True)
        os.system('> requirements.txt')

        if cfg.python3:
            os.system('cat ./scripts/python_packages/basic_python_packages.txt >> ./requirements.txt')
            status_str += "--python3, "

        if cfg.open3d:
            os.system('cat ./scripts/python_packages/open3d.txt >> ./requirements.txt')
            status_str += "--open3d, "

        if cfg.opencv_python:
            os.system('cat ./scripts/python_packages/opencv-python.txt >> ./requirements.txt')
            status_str += "--opencv_python, "

            if cfg.opencv_contrib_python:
                os.system('cat ./scripts/python_packages/opencv-contrib-python.txt >> ./requirements.txt')
                status_str += "--opencv_contrib_python, "

        os.system('chmod u+x ./scripts/python_packages/install_python_packages.sh')
        os.system('./scripts/python_packages/install_python_packages.sh')

    print(status_str)


if __name__ == '__main__':
    main()
