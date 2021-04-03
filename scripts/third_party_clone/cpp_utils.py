import os
import shutil
import multiprocessing


class install_cpp_utils:
    def __init__(self, d):
        self.d = d
        self.install_dir = "./third_party"

    def run(self):
        self.__install_csv_parser()
        self.__install_spdlog()

    def __install_spdlog(self):
        # https://github.com/gabime/spdlog.git
        path = self.install_dir + "/spdlog/spdlog"
        shutil.rmtree(path, ignore_errors=True)

        os.system(
            "git clone https://github.com/gabime/spdlog.git " + path)

        os.system("mkdir " + path + "/../build")
        os.chdir(path + "/../build")
        os.system("cmake ../spdlog")

        num_cpu_cores = multiprocessing.cpu_count()
        os.system("make -j" + str(num_cpu_cores-1))

    def __install_csv_parser(self):
        # https://github.com/ben-strasser/fast-cpp-csv-parser
        path = self.install_dir + "/fast-cpp-csv-parser"
        shutil.rmtree(path, ignore_errors=True)

        os.system(
            "git clone https://github.com/ben-strasser/fast-cpp-csv-parser.git " + path)
        shutil.copyfile(path + "/csv.h", "./src/log/csv.h")
