import os
import multiprocessing


class install_glad:
    def __init__(self, d, version_num, linux_password):
        self.d = d
        self.version_num = version_num
        self.install_dir = "./third_party/glad"
        self.pw = linux_password

    def run(self):
        self.pw.redeem()

        # Remove any pre-installed GLAD
        os.system("sudo rm -rf ./third_party/glad")

        # Download GLAD source code
        os.system("mkdir " + self.install_dir)
        os.system("git clone https://github.com/Dav1dde/glad.git " + self.install_dir + "/glad")

        # CMake configure
        os.system("mkdir " + self.install_dir + "/build")
        os.system("mkdir " + self.install_dir + "/install")
        os.chdir(self.install_dir + "/build")

        exec_string = "cmake ../glad -DCMAKE_INSTALL_PREFIX=../install"

        if self.d:
            exec_string += " -DCMAKE_BUILD_TYPE=Debug"

        return_code = os.system(exec_string)
        if return_code != 0:
            print("Error occured in building GLAD!")
            return

        # Build
        self.pw.redeem()
        num_cpu_cores = multiprocessing.cpu_count()
        os.system("make -j" + str(num_cpu_cores-1)) # No sudo make install here.

        os.system("cp -r include ../install/include")
        os.system("cp -r src ../install/src")
        os.system("cp libglad.a ../install/libglad.a")

        # Delete source files
        os.chdir("../../../")
