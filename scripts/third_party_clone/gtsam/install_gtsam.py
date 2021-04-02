import os
import multiprocessing


class install_gtsam:
    def __init__(self, d, version_num):
        self.d = d
        self.version_num = version_num
        self.install_dir = "./third_party/GTSAM"

    def run(self):
        # Remove any pre-installed GTSAM
        os.system("rm -rf ./third_party/GTSAM")

        # Install dependencies
        print("GTSAM requires libboost-all-dev (Boost)")
        os.system("sudo sudo apt install -y libboost-all-dev")

        # Download GTSAM source code
        os.system("mkdir " + self.install_dir)
        os.system("wget -O " + self.install_dir +
                  "/gtsam.zip https://github.com/borglab/gtsam/archive/refs/tags/" + self.version_num + ".zip")
        os.system("unzip " + self.install_dir +
                  "/gtsam.zip -d " + self.install_dir)

        # CMake configure
        os.system("mkdir " + self.install_dir + "/build")
        os.chdir(self.install_dir + "/build")

        exec_string = "cmake ../gtsam-" + self.version_num

        if self.d:
            exec_string += " -DCMAKE_BUILD_TYPE=Debug"

        return_code = os.system(exec_string)
        if return_code != 0:
            print("Error occured in building GTSAM!")
            return

        # Build
        num_cpu_cores = multiprocessing.cpu_count()
        os.system("make check -j" + str(num_cpu_cores-1))
        os.system("make -j" + str(num_cpu_cores-1))

        # Delete source files
        os.chdir("../")
        os.system("rm -rf gtsam.zip")
