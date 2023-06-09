import os
import sys
import urllib.request
import urllib.error


def build_and_install_easy_profiler(cfg_easy_profiler, cfg_basic):
    """_summary_

    Args:
        cfg_easy_profiler (dict): Config dictionary for easy_profiler
        cfg_basic (BasicConfig): Config object for basic config for build and install
    """

    base_path = cfg_basic.base_path
    install_in_system = cfg_basic.install_in_system
    os_name = cfg_basic.os_name
    nproc = cfg_basic.nproc
    password = cfg_basic.pw
    enable_debug = cfg_basic.d

    if os_name == "Linux":
        install_easy_profiler_linux(
            cfg_easy_profiler,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )
    elif os_name == "Windows":
        install_easy_profiler_macos(
            cfg_easy_profiler,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )
    elif os_name == "Darwin":
        install_easy_profiler_windows(
            cfg_easy_profiler,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )


def install_easy_profiler_linux(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    """Build easy_profiler on Linux (Release mode only - since most of the time only the fast loggers are desired)

    Args:
        cfg (dict): Config object for building Easy-profiler
        base_path (str): Base path of the project
        install_in_system (bool): Boolean flag to install Easy-profiler in system (/usr/local) or in the project directory
        os_name (str): Name of the OS
        nproc (str): Number of processors
        password (Password): Password object to get sudo password
        enable_debug (bool): Boolean flag to enable debug mode
    """

    os.chdir(base_path)

    version_num = cfg["version_num"]
    debug_build_flags = ""
    release_build_flags = ""

    for flag in cfg["cmake_flags"]["debug"]:
        debug_build_flags += flag
        debug_build_flags += " "

    for flag in cfg["cmake_flags"]["release"]:
        release_build_flags += flag
        release_build_flags += " "

    try:
        os.system(password.sudo() + "apt-get -y install qt5-default libqt5widgets5")
        os.system(password.sudo() + "rm -rf ./thirdparty/easy_profiler")

        os.makedirs("./thirdparty/easy_profiler")
        os.chdir("./thirdparty/easy_profiler")

        try:
            urllib.request.urlretrieve(
                "https://github.com/yse/easy_profiler/archive/refs/tags/v"
                + version_num
                + ".zip",
                "./easy_profiler.zip",
            )
        except urllib.error.HTTPError as e:
            raise Exception("Easy-profiler: cloning failed")

        os.system("unzip ./easy_profiler.zip -d .")

        os.makedirs("./build/Release", exist_ok=True)
        os.makedirs("./install/Release", exist_ok=True)
        os.chdir("./build/Release")

        exec_string = "cmake ../../easy_profiler-" + version_num + " -GNinja"

        if install_in_system:
            if (
                os.system(
                    exec_string + " -DCMAKE_BUILD_TYPE=Release " + release_build_flags
                )
                != 0
            ):
                raise Exception("Easy-profiler: cmake configuration failed")
        else:
            if (
                os.system(
                    exec_string
                    + " -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../install/Release "
                    + release_build_flags
                )
                != 0
            ):
                raise Exception("Easy-profiler: cmake configuration failed")

        if os.system("ninja " + nproc) != 0:
            raise Exception("Easy-profiler: ninja failed")

        if os.system(password.sudo() + "ninja install") != 0:
            raise Exception("Easy-profiler: ninja install failed")

        if not install_in_system:
            # Copy lib files to system
            os.chdir("../../install/Release/lib")
            os.system(
                password.sudo()
                + "cp libeasy_profiler.so /usr/lib/x86_64-linux-gnu/libeasy_profiler.so"
            )

        os.chdir("../../../")
        os.system(password.sudo() + "rm -rf ./build")
        os.system(password.sudo() + "rm -rf easy_profiler-" + version_num)

    except Exception as e:
        print("")
        sys.exit(e)


def install_easy_profiler_windows(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    print("easy_profiler: Windows is not supported yet")
    sys.exit(1)


def install_easy_profiler_macos(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    print("easy_profiler: MacOS is not supported yet")
    sys.exit(1)
