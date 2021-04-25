import os
import multiprocessing


class install_ceres_solver:
    def __init__(self, d, version_num):
        self.d = d
        self.version_num = version_num
        self.install_dir = "./third_party/ceres-solver"

    def run(self):
        # Remove any pre-installed Ceres-solver
        os.system("rm -rf ./third_party/ceres-solver")

        # Install dependencies
        print("Ceres-solver installation dependencies: libgoogle-glog-dev (glog), libgflags-dev (gflags), libatlas-base-dev (LAPACK & BLAS), libeigen3-dev (Eigen3), libsuitesparse-dev (SuiteSparse)")
        os.system(
            "sudo apt-get install -y libgoogle-glog-dev libgflags-dev libatlas-base-dev libeigen3-dev libsuitesparse-dev")

        # Download source code
        os.system("mkdir " + self.install_dir)
        os.system("wget -O " + self.install_dir +
                  "/ceres-solver.tar.gz http://ceres-solver.org/ceres-solver-" + self.version_num + ".tar.gz")
        os.system("tar zxf " + self.install_dir +
                  "/ceres-solver.tar.gz -C " + self.install_dir)

        # CMake configure
        os.system("mkdir " + self.install_dir + "/ceres-bin")
        os.system("mkdir " + self.install_dir + "/install")

        os.chdir(self.install_dir + "/ceres-bin")

        exec_string = "cmake ../ceres-solver-" + self.version_num + \
            " -DEXPORT_BUILD_DIR=ON -DCMAKE_INSTALL_PREFIX=../install"

        if self.d:
            exec_string += " -DCMAKE_BUILD_TYPE=Debug"

        return_code = os.system(exec_string)
        if return_code != 0:
            print("Error occured in building Ceres-solver!")
            return

        # Build
        num_cpu_cores = multiprocessing.cpu_count()
        os.system("make -j" + str(num_cpu_cores-1))
        os.system("make test")
        os.system("sudo make install")
        # No `make install`, since this will install in system.

        # Delete source files
        os.chdir("../")
        os.system("rm -rf ceres-solver.tar.gz")

        os.chdir("../../")
