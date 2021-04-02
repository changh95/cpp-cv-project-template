import os
import multiprocessing


class install_opencv:
    def __init__(self, version_num, build_contrib):
        self.version_num = version_num
        self.install_dir = "./third_party/opencv"
        self.build_contrib = build_contrib

    def run(self):
        # Remove any pre-installed OpenCV
        os.system("rm -rf ./third_party/opencv*")

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
        os.chdir(self.install_dir + "/build")

        if self.build_contrib:
            os.system(
                "cmake -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-" + self.version_num + "/modules ../opencv-" + self.version_num)
        else:
            os.system("cmake ../opencv-" + self.version_num)

        # Build
        num_cpu_cores = multiprocessing.cpu_count()
        os.system("make -j" + str(num_cpu_cores))

        # Delete source files
        os.chdir("../")
        os.system("rm -rf opencv.zip")

        if self.build_contrib:
            os.system("rm -rf opencv_contrib.zip")
