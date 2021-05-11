import os
import multiprocessing


class install_pcl:
    def __init__(self, d, version_num, linux_password):
        self.d = d
        self.version_num = version_num
        self.install_dir = "./third_party/pcl"
        self.pw = linux_password

    def run(self):
        self.pw.redeem()

        # Install dependencies
        print(
            "PCL installation dependencies: libboost-all-dev (Boost), libflann-dev (FLANN), ligblew-dev (GLEW)")
        os.system(
            "sudo apt install -y libboost-all-dev libflann-dev libglew-dev")

        # Remove any pre-installed PCL
        os.system("sudo rm -rf ./third_party/pcl")

        # Download PCL source code
        os.system("mkdir " + self.install_dir)
        os.system("wget -O " + self.install_dir + "/pcl.zip https://github.com/PointCloudLibrary/pcl/archive/refs/tags/pcl-" +
                  self.version_num + ".zip")
        os.system("unzip " + self.install_dir +
                  "/pcl.zip -d " + self.install_dir)

        # CMake configure
        os.system("mkdir " + self.install_dir + "/build")
        os.system("mkdir " + self.install_dir + "/install")
        os.chdir(self.install_dir + "/build")

        # Disable visualization module due to lack of VTK support
        # TODO: Enable visualization module
        exec_string = "cmake ../pcl-pcl-" + self.version_num + " -DBUILD_visualization=OFF -DCMAKE_INSTALL_PREFIX=../install -DEIGEN_ROOT=../../Eigen/install/"

        if self.d:
            exec_string += " -DCMAKE_BUILD_TYPE=Debug"

        return_code = os.system(exec_string)
        if return_code != 0:
            print("Error occured in building PCL!")
            return

        # Build
        self.pw.redeem()
        num_cpu_cores = multiprocessing.cpu_count()
        os.system("make -j" + str(num_cpu_cores-1))
        os.system("sudo make install -j" + str(num_cpu_cores-1))

        # Delete source files
        os.chdir("../")
        os.system("rm -rf pcl.zip")

        os.chdir("../../")
