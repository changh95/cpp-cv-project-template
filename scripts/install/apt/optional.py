import os

def install_apt_optional(cfg):
    """Installs optional packages for the given platform."

    Args:
        cfg (Config): Config object for the current build
    """    
    
    if cfg.basic_config.os_name == "Linux":
        install_packages_linux(cfg)
    elif cfg.os_name == "Darwin":
        install_packages_mac(cfg)
    elif cfg.os_name == "Windows":
        install_packages_windows(cfg)


def install_packages_linux(cfg):
    """Installs optional packages for Linux.

    Args:
        cfg (Config): Config object for the current build
    """    
    
    libs_string = ""

    if cfg.boost:
        libs_string += "libboost-all-dev "
    if cfg.yaml_cpp:
        libs_string += "libyaml-cpp-dev "
    if cfg.doxygen:
        libs_string += "doxygen "
    if cfg.png:
        libs_string += "libpng-dev "
    if cfg.tiff:
        libs_string += "libtiff-dev "
    if cfg.jpeg:
        libs_string += "libjpeg-dev "
    if cfg.zlib:
        libs_string += "zlib1g-dev "
    if cfg.glut:
        libs_string += "freeglut3-dev "
    if cfg.glew:
        libs_string += "libglew-dev "
    if cfg.glfw:
        libs_string += "libglfw3-dev "
    if cfg.glm:
        libs_string += "libglm-dev "
    if cfg.json:
        libs_string += "libjsoncpp-dev "
    if cfg.glog:
        libs_string += "libgoogle-glog-dev "
    if cfg.gflags:
        libs_string += "libgflags-dev "

    os.system(cfg.basic_config.pw.sudo() + "apt-get -y install " + libs_string)

def install_packages_mac(cfg):
    """Installs optional packages for Mac.

    Args:
        cfg (Config): Config object for the current build
    """    
    
    print("Unimplemented on Mac")
    import sys; sys.exit()
    

def install_packages_windows(cfg):
    """Installs optional packages for Windows.

    Args:
        cfg (Config): Config object for the current build
    """    
    
    print("Unimplemented on Windows")
    import sys; sys.exit()