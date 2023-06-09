import os

def install_apt_essential(cfg):
    """Installs essential packages for the current platform.

    Args:
        cfg (Config): Config object
    """    
    
    platform = cfg.basic_config.os_name
    password = cfg.basic_config.pw

    if platform == "Linux":
        install_linux_packages(password)
    elif platform == "Darwin":
        install_mac_packages(password)
    elif platform == "Windows":
        install_windows_packages(password)

def install_linux_packages(password):
    """Installs essential packages for Linux.

    Args:
        password (Password): Password object for sudo access
    """    
    
    libs_string = "unzip wget curl git build-essential cmake ninja-build gcc clang-format"
    os.system(password.sudo() + "apt-get -y install " + libs_string)
    
def install_mac_packages(password):
    """Installs essential packages for Mac.

    Args:
        password (Password): Password object for sudo access
    """    
    
    print("Unimplemented on Mac")
    import sys; sys.exit()
    #libs_string = "unzip wget curl git cmake ninja clang-format"
    #os.system("brew install " + libs_string)
    
def install_windows_packages(password):
    """Installs essential packages for Windows.

    Args:
        password (Password): Password object for sudo access
    """   
    
    print("Unimplemented on Windows")
    import sys; sys.exit()
    #libs_string = "unzip wget curl git cmake ninja clang-format"
    #os.system("choco install " + libs_string)