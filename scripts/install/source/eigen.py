import os
import sys
import urllib.request
import urllib.error


def build_and_install_eigen(cfg_eigen, cfg_basic):
    """_summary_

    Args:
        cfg_eigen (dict): Config dictionary for eigen
        cfg_basic (BasicConfig): Config object for basic config for build and install
    """

    base_path = cfg_basic.base_path
    install_in_system = cfg_basic.install_in_system
    os_name = cfg_basic.os_name
    nproc = cfg_basic.nproc
    password = cfg_basic.pw
    enable_debug = cfg_basic.d

    if os_name == "Linux":
        install_eigen_linux(
            cfg_eigen,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )
    elif os_name == "Windows":
        install_eigen_macos(
            cfg_eigen,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )
    elif os_name == "Darwin":
        install_eigen_windows(
            cfg_eigen,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )


def install_eigen_linux(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    """Build eigen on Linux

    Args:
        cfg (dict): Config object for building Eigen
        base_path (str): Base path of the project
        install_in_system (bool): Boolean flag to install Eigen in system (/usr/local) or in the project directory
        os_name (str): Name of the OS
        nproc (str): Number of processors
        password (Password): Password object to get sudo password
        enable_debug (bool): Boolean flag to enable debug mode
    """
    
    os.chdir(base_path)

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
        os.system(password.sudo() + "apt-get -y install libblas-dev")
        os.system(password.sudo() + "apt-get -y install libatlas-base-dev")
        os.system(password.sudo() + "apt-get -y install liblapack-dev")

        os.system(password.sudo() + "rm -rf ./thirdparty/eigen")

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

        if os.system("ninja" + nproc) != 0:
            raise Exception("Eigen: ninja failed")

        if os.system(password.sudo() + "ninja install") != 0:
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

            if os.system("ninja" + nproc) != 0:
                raise Exception("Eigen: ninja failed")

            if os.system(password.sudo() + "ninja install") != 0:
                raise Exception("Eigen: ninja install failed")

        os.chdir("../../")
        os.system(password.sudo() + "rm -rf ./build")
        os.system(password.sudo() + "rm -rf eigen-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)


def install_eigen_windows(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    print("eigen: Windows is not supported yet")
    sys.exit(1)


def install_eigen_macos(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    print("eigen: MacOS is not supported yet")
    sys.exit(1)
