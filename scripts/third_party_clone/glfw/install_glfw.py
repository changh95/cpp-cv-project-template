import os
import multiprocessing


class install_glfw:
    def __init__(self, d, version_num, linux_password):
        self.d = d
        self.version_num = version_num
        self.install_dir = "./third_party/glfw"
        self.pw = linux_password

    def run(self):
        self.pw.redeem()

        # Remove any pre-installed GLFW
        os.system("sudo rm -rf ./third_party/glfw")

        # Download GLFW source code
        os.system("mkdir " + self.install_dir)
        os.system("wget -O " + self.install_dir + "/glfw.zip https://github.com/glfw/glfw/archive/refs/tags/" + self.version_num + ".zip")
        os.system("unzip " + self.install_dir + "/glfw.zip -d " + self.install_dir)

        # CMake configure
        os.system("mkdir " + self.install_dir + "/build")
        os.system("mkdir " + self.install_dir + "/install")
        os.chdir(self.install_dir + "/build")

        exec_string = "cmake ../glfw-" + self.version_num + " -DCMAKE_INSTALL_PREFIX=../install"

        if self.d:
            exec_string += " -DCMAKE_BUILD_TYPE=Debug"

        return_code = os.system(exec_string)
        if return_code != 0:
            print("Error occured in building GLFW!")
            return

        # Build
        self.pw.redeem()
        num_cpu_cores = multiprocessing.cpu_count()
        os.system("make -j" + str(num_cpu_cores-1))
        self.pw.redeem()
        os.system("sudo make install -j" + str(num_cpu_cores-1))

        # Delete source files
        os.chdir("../")
        os.system("rm -rf glfw.zip")

        os.chdir("../../")
