import os
import multiprocessing


class install_eigen:
    def __init__(self, d, version_num):
        self.d = d
        self.version_num = version_num
        self.install_dir = "./third_party/Eigen"

    def run(self):
        # Remove any pre-installed Eigen
        os.system("rm -rf ./third_party/Eigen")

        # Download Eigen source code
        os.system("mkdir " + self.install_dir)
        os.system("wget -O " + self.install_dir + "/eigen.zip https://gitlab.com/libeigen/eigen/-/archive/" +
                  self.version_num + "/eigen-" + self.version_num + ".zip")
        os.system("unzip " + self.install_dir +
                  "/eigen.zip -d " + self.install_dir)

        # CMake configure
        os.system("mkdir " + self.install_dir + "/build")
        os.chdir(self.install_dir + "/build")

        exec_string = "cmake ../eigen-" + self.version_num

        if self.d:
            exec_string += " -DCMAKE_BUILD_TYPE=Debug"

        return_code = os.system(exec_string)
        if return_code != 0:
            print("Error occured in building Eigen!")
            return

        # Build
        num_cpu_cores = multiprocessing.cpu_count()
        os.system("make -j" + str(num_cpu_cores-1))

        # Delete source files
        os.chdir("../")
        os.system("rm -rf eigen.zip")
