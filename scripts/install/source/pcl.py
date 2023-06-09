import os
import sys
import urllib.request
import urllib.error


def build_and_install_pcl(cfg_pcl, cfg_basic):
    """_summary_

    Args:
        cfg_pcl (dict): Config dictionary for pcl
        cfg_basic (BasicConfig): Config object for basic config for build and install
    """

    base_path = cfg_basic.base_path
    install_in_system = cfg_basic.install_in_system
    os_name = cfg_basic.os_name
    nproc = cfg_basic.nproc
    password = cfg_basic.pw
    enable_debug = cfg_basic.d

    if os_name == "Linux":
        install_pcl_linux(
            cfg_pcl,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )
    elif os_name == "Windows":
        install_pcl_macos(
            cfg_pcl,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )
    elif os_name == "Darwin":
        install_pcl_windows(
            cfg_pcl,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )


def install_pcl_linux(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    """Build pcl on Linux

    Args:
        cfg (dict): Config object for building PCL
        base_path (str): Base path of the project
        install_in_system (bool): Boolean flag to install PCL in system (/usr/local) or in the project directory
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
        os.system(password.sudo() + "apt-get -y install libflann-dev")
        os.system(password.sudo() + "apt-get -y install libglew-dev")

        os.system(password.sudo() + "rm -rf ./thirdparty/pcl")

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

        if os.system("ninja" + nproc) != 0:
            raise Exception("PCL: ninja failed")

        if os.system(password.sudo() + "ninja install") != 0:
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

            if os.system("ninja" + nproc) != 0:
                raise Exception("PCL: ninja failed")

            if os.system(password.sudo() + "ninja install") != 0:
                raise Exception("PCL: ninja install failed")

        os.chdir("../../")
        os.system(password.sudo() + "rm -rf ./build")
        os.system(password.sudo() + "rm -rf pcl-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)




def install_pcl_windows(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    print("pcl: Windows is not supported yet")
    sys.exit(1)


def install_pcl_macos(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    print("pcl: MacOS is not supported yet")
    sys.exit(1)
