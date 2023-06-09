import os
import sys
import urllib.request
import urllib.error


def build_and_install_gtsam(cfg_gtsam, cfg_basic):
    """_summary_

    Args:
        cfg_gtsam (dict): Config dictionary for gtsam
        cfg_basic (BasicConfig): Config object for basic config for build and install
    """

    base_path = cfg_basic.base_path
    install_in_system = cfg_basic.install_in_system
    os_name = cfg_basic.os_name
    nproc = cfg_basic.nproc
    password = cfg_basic.pw
    enable_debug = cfg_basic.d

    if os_name == "Linux":
        install_gtsam_linux(
            cfg_gtsam,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )
    elif os_name == "Windows":
        install_gtsam_macos(
            cfg_gtsam,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )
    elif os_name == "Darwin":
        install_gtsam_windows(
            cfg_gtsam,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )


def install_gtsam_linux(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    """Build gtsam on Linux

    Args:
        cfg (dict): Config object for building GTSAM
        base_path (str): Base path of the project
        install_in_system (bool): Boolean flag to install GTSAM in system (/usr/local) or in the project directory
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
        os.system(password.sudo() + "apt-get -y install libboost-all-dev")
        os.system(password.sudo() + "rm -rf ./thirdparty/gtsam")

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

        if os.system("ninja" + nproc) != 0:
            raise Exception("GTSAM: ninja failed")

        if os.system(password.sudo() + "ninja install") != 0:
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

            if os.system("ninja" + nproc) != 0:
                raise Exception("GTSAM: ninja failed")

            if os.system(password.sudo() + "ninja install") != 0:
                raise Exception("GTSAM: ninja install failed")

        os.chdir("../../")
        os.system(password.sudo() + "rm -rf ./build")
        os.system(password.sudo() + "rm -rf gtsam-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)


def install_gtsam_windows(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    print("gtsam: Windows is not supported yet")
    sys.exit(1)


def install_gtsam_macos(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    print("gtsam: MacOS is not supported yet")
    sys.exit(1)
