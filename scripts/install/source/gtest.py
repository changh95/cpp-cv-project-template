import os
import sys
import urllib.request
import urllib.error


def build_and_install_gtest(cfg_gtest, cfg_basic):
    """_summary_

    Args:
        cfg_gtest (dict): Config dictionary for gtest
        cfg_basic (BasicConfig): Config object for basic config for build and install
    """

    base_path = cfg_basic.base_path
    install_in_system = cfg_basic.install_in_system
    os_name = cfg_basic.os_name
    nproc = cfg_basic.nproc
    password = cfg_basic.pw
    enable_debug = cfg_basic.d

    if os_name == "Linux":
        install_gtest_linux(
            cfg_gtest,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )
    elif os_name == "Windows":
        install_gtest_macos(
            cfg_gtest,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )
    elif os_name == "Darwin":
        install_gtest_windows(
            cfg_gtest,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )


def install_gtest_linux(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    """Build gtest on Linux (Release mode only - since most of the time only the fast loggers are desired)

    Args:
        cfg (dict): Config object for building GTest
        base_path (str): Base path of the project
        install_in_system (bool): Boolean flag to install GTest in system (/usr/local) or in the project directory
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
        os.system(password.sudo() + "rm -rf ./thirdparty/gtest")

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

        if os.system("ninja" + nproc) != 0:
            raise Exception("GTest: ninja failed")
        if os.system("ninja test") != 0:
            raise Exception("GTest: ceres-solver unit test failed")
        if os.system(password.sudo() + "ninja install") != 0:
            raise Exception("GTest: ninja install failed")

        os.chdir("../../")
        os.system("sudo rm -rf ./build")
        os.system("sudo rm -rf googletest-release-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)


def install_gtest_windows(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    print("gtest: Windows is not supported yet")
    sys.exit(1)


def install_gtest_macos(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    print("gtest: MacOS is not supported yet")
    sys.exit(1)
