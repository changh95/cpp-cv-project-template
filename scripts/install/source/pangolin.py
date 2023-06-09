import os
import sys
import urllib.request
import urllib.error


def build_and_install_pangolin(cfg_pangolin, cfg_basic):
    """_summary_

    Args:
        cfg_pangolin (dict): Config dictionary for pangolin
        cfg_basic (BasicConfig): Config object for basic config for build and install
    """

    base_path = cfg_basic.base_path
    install_in_system = cfg_basic.install_in_system
    os_name = cfg_basic.os_name
    nproc = cfg_basic.nproc
    password = cfg_basic.pw
    enable_debug = cfg_basic.d

    if os_name == "Linux":
        install_pangolin_linux(
            cfg_pangolin,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )
    elif os_name == "Windows":
        install_pangolin_macos(
            cfg_pangolin,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )
    elif os_name == "Darwin":
        install_pangolin_windows(
            cfg_pangolin,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )


def install_pangolin_linux(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    """Build pangolin on Linux

    Args:
        cfg (dict): Config object for building Pangolin
        base_path (str): Base path of the project
        install_in_system (bool): Boolean flag to install Pangolin in system (/usr/local) or in the project directory
        os_name (str): Name of the OS
        nproc (str): Number of processors
        password (Password): Password object to get sudo password
        enable_debug (bool): Boolean flag to enable debug mode
    """
    
    os.chdir(base_path)

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
        os.system(password.sudo() + "apt-get -y install libglvnd-dev")
        os.system(password.sudo() + "apt-get -y install libgl1-mesa-dev")
        os.system(password.sudo() + "apt-get -y install libegl1-mesa-dev")

        os.system(password.sudo() + "rm -rf ./thirdparty/pangolin")

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

        if os.system("ninja" + nproc) != 0:
            raise Exception("Pangolin: ninja failed")

        if os.system(password.sudo() + "ninja install") != 0:
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

                if os.system("ninja" + nproc) != 0:
                    raise Exception("Pangolin: ninja failed")

                if os.system(password.sudo() + "ninja install") != 0:
                    raise Exception("Pangolin: ninja install failed")

        os.chdir("../../")
        os.system(password.sudo() + "rm -rf ./build")
        os.system(password.sudo() + "rm -rf Pangolin-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)



def install_pangolin_windows(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    print("pangolin: Windows is not supported yet")
    sys.exit(1)


def install_pangolin_macos(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    print("pangolin: MacOS is not supported yet")
    sys.exit(1)
