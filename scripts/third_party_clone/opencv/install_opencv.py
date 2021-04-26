import os
import multiprocessing


class install_opencv:
    def __init__(self, d, version_num, build_contrib):
        self.d = d
        self.version_num = version_num
        self.install_dir = "./third_party/opencv"
        self.build_contrib = build_contrib

    def run(self):
        # Remove any pre-installed OpenCV
        os.system("sudo rm -rf ./third_party/opencv*")

        # Download opencv source code
        os.system("mkdir " + self.install_dir)
        os.system("wget -O " + self.install_dir + "/opencv.zip https://github.com/opencv/opencv/archive/" +
                  self.version_num + ".zip")
        os.system("unzip " + self.install_dir +
                  "/opencv.zip -d " + self.install_dir)

        if self.build_contrib:
            os.system("wget -O " + self.install_dir + "/opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/" +
                      self.version_num + ".zip")
            os.system("unzip " + self.install_dir +
                      "/opencv_contrib.zip -d " + self.install_dir)

        # CMake configure
        os.system("mkdir " + self.install_dir + "/build")
        os.system("mkdir " + self.install_dir + "/install")
        os.chdir(self.install_dir + "/build")

        # We enable non-free algorithms (e.g. SIFT, SURF...)
        exec_string = "cmake ../opencv-" + self.version_num + " -DOPENCV_ENABLE_NONFREE=ON -DCMAKE_INSTALL_PREFIX=../install"

        if self.build_contrib:
            exec_string += " -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-" + \
                self.version_num + "/modules"

        if self.d:
            exec_string += " -DCMAKE_BUILD_TYPE=Debug"

        return_code = os.system(exec_string)
        if return_code != 0:
            print("Error occured in building OpenCV!")
            return

        # Build
        num_cpu_cores = multiprocessing.cpu_count()
        os.system("make -j" + str(num_cpu_cores-1))
        os.system("sudo make install")

        # Delete source files
        os.chdir("../")
        os.system("rm -rf opencv.zip")

        if self.build_contrib:
            os.system("rm -rf opencv_contrib.zip")

        os.chdir("../../")
