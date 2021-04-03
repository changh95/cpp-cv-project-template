import os
import multiprocessing


class install_pcl:
    def __init__(self, d, version_num):
        self.d = d
        self.version_num = version_num
        self.install_dir = "./third_party/pcl"

    def run(self):
        # Install dependencies
        print(
            "PCL installation dependencies: libboost-all-dev (Boost), libflann-dev (FLANN)")
        os.system(
            "sudo apt install -y libboost-all-dev libflann-dev")

        # Remove any pre-installed PCL
        os.system("rm -rf ./third_party/pcl")

        # Download PCL source code
        os.system("mkdir " + self.install_dir)
        os.system("wget -O " + self.install_dir + "/pcl.zip https://github.com/PointCloudLibrary/pcl/archive/refs/tags/pcl-" +
                  self.version_num + ".zip")
        os.system("unzip " + self.install_dir +
                  "/pcl.zip -d " + self.install_dir)

        # CMake configure
        os.system("mkdir " + self.install_dir + "/build")
        os.chdir(self.install_dir + "/build")

        exec_string = "cmake ../pcl-pcl-" + self.version_num + " -DBUILD_visualization=OFF"

        if self.d:
            exec_string += " -DCMAKE_BUILD_TYPE=Debug"

        return_code = os.system(exec_string)
        if return_code != 0:
            print("Error occured in building PCL!")
            return

        # Build
        num_cpu_cores = multiprocessing.cpu_count()
        os.system("make -j" + str(num_cpu_cores-1))

        # Delete source files
        os.chdir("../")
        os.system("rm -rf pcl.zip")

        os.chdir("../../")
