import os
import sys
import urllib.request
import urllib.error


def build_and_install_ceres(cfg_ceres, cfg_basic):
    """_summary_

    Args:
        cfg_ceres (dict): Config dictionary for ceres
        cfg_basic (BasicConfig): Config object for basic config for build and install
    """

    base_path = cfg_basic.base_path
    install_in_system = cfg_basic.install_in_system
    os_name = cfg_basic.os_name
    nproc = cfg_basic.nproc
    password = cfg_basic.pw
    enable_debug = cfg_basic.d

    if os_name == "Linux":
        install_ceres_linux(
            cfg_ceres,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )
    elif os_name == "Windows":
        install_ceres_macos(
            cfg_ceres,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )
    elif os_name == "Darwin":
        install_ceres_windows(
            cfg_ceres,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )


def install_ceres_linux(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    """Build ceres on Linux

    Args:
        cfg (dict): Config object for building Ceres-solver
        base_path (str): Base path of the project
        install_in_system (bool): Boolean flag to install Ceres-solver in system (/usr/local) or in the project directory
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
        os.system(password.sudo() + "apt-get -y install libgoogle-glog-dev")
        os.system(password.sudo() + "apt-get -y install libgflags-dev")
        os.system(password.sudo() + "apt-get -y install libatlas-base-dev")
        os.system(password.sudo() + "apt-get -y install libsuitesparse-dev")
        os.system(password.sudo() + "apt-get -y install libpthread-stubs0-dev")

        os.system(password.sudo() + "rm -rf ./thirdparty/ceres")

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

        if os.system("ninja" + nproc) != 0:
            raise Exception("Ceres-solver: ninja failed")

        # if os.system("ninja test") != 0:
        #     raise Exception("Ceres-solver: ceres-solver unit test failed")

        if os.system(password.sudo() + "ninja install") != 0:
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

            if os.system("ninja" + nproc) != 0:
                raise Exception("Ceres-solver: ninja failed")

            # if os.system("ninja test") != 0:
            #     raise Exception("Ceres-solver: ceres-solver unit test failed")

            if os.system(password.sudo() + "ninja install") != 0:
                raise Exception("Ceres-solver: ninja install failed")

        os.chdir("../../")
        os.system(password.sudo() + "rm -rf ./build")
        os.system(password.sudo() + "rm -rf ceres-solver-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)


def install_ceres_windows(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    print("ceres: Windows is not supported yet")
    sys.exit(1)


def install_ceres_macos(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    print("ceres: MacOS is not supported yet")
    sys.exit(1)
