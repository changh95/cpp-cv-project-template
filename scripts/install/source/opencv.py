import os
import sys
import urllib.request
import urllib.error


def build_and_install_opencv(cfg_opencv, cfg_basic):
    """_summary_

    Args:
        cfg_opencv (dict): Config dictionary for opencv
        cfg_basic (BasicConfig): Config object for basic config for build and install
    """

    base_path = cfg_basic.base_path
    install_in_system = cfg_basic.install_in_system
    os_name = cfg_basic.os_name
    nproc = cfg_basic.nproc
    password = cfg_basic.pw
    enable_debug = cfg_basic.d

    if os_name == "Linux":
        install_opencv_linux(
            cfg_opencv,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )
    elif os_name == "Windows":
        install_opencv_macos(
            cfg_opencv,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )
    elif os_name == "Darwin":
        install_opencv_windows(
            cfg_opencv,
            base_path,
            install_in_system,
            os_name,
            nproc,
            password,
            enable_debug,
        )


def install_opencv_linux(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    """Build opencv on Linux

    Args:
        cfg (dict): Config object for building OpenCV
        base_path (str): Base path of the project
        install_in_system (bool): Boolean flag to install OpenCV in system (/usr/local) or in the project directory
        os_name (str): Name of the OS
        nproc (str): Number of processors
        password (Password): Password object to get sudo password
        enable_debug (bool): Boolean flag to enable debug mode
    """

    # TODO: Check if we need contrib?
    # TODO: Check whether we use OpenCV 3 or 4.
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
        os.system(password.sudo() + "apt-get -y install ffmpeg")
        os.system(password.sudo() + "apt-get -y install libgtk2.0-dev")
        os.system(password.sudo() + "apt-get -y install pkg-config")
        os.system(password.sudo() + "apt-get -y install libavcodec-dev")
        os.system(password.sudo() + "apt-get -y install libswscale-dev")
        os.system(password.sudo() + "apt-get -y install python-dev")
        os.system(password.sudo() + "apt-get -y install python-numpy")
        os.system(password.sudo() + "apt-get -y install libtbb2")
        os.system(password.sudo() + "apt-get -y install libtbb-dev")
        os.system(password.sudo() + "apt-get -y install libjpeg-dev")
        os.system(password.sudo() + "apt-get -y install libpng-dev")
        os.system(password.sudo() + "apt-get -y install libtiff-dev")
        os.system(password.sudo() + "apt-get -y install libdc1394-22-dev")
        os.system(password.sudo() + "rm -rf ./thirdparty/opencv")

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

        if os.system("ninja" + nproc) != 0:
            raise Exception("OpenCV: ninja failed")

        if os.system(password.sudo() + "ninja install") != 0:
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

            if os.system("ninja" + nproc) != 0:
                raise Exception("OpenCV: ninja failed")

            if os.system(password.sudo() + "ninja install") != 0:
                raise Exception("OpenCV: ninja install failed")

        os.chdir("../../")
        os.system(password.sudo() + "rm -rf ./build")
        os.system(password.sudo() + "rm -rf opencv-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)


def install_opencv_windows(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    print("opencv: Windows is not supported yet")
    sys.exit(1)


def install_opencv_macos(
    cfg, base_path, install_in_system, os_name, nproc, password, enable_debug
):
    print("opencv: MacOS is not supported yet")
    sys.exit(1)
