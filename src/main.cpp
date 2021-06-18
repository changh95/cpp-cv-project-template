#include <iostream>
#include <pangolin/config.h>

#ifdef EIGEN_DEVELOP
#include <Eigen/Dense>
#endif

#ifdef CERES_DEVELOP
#include <ceres/ceres.h>
#endif

#ifdef OPENCV_DEVELOP
#include <opencv2/core.hpp>
#endif

#ifdef PCL_DEVELOP
#include <pcl/pcl_base.h>
#include <pcl/pcl_config.h>
#endif

#ifdef GTSAM_DEVELOP
#include <gtsam/global_includes.h>
#endif

#ifdef SPDLOG_DEVELOP
#include <fstream>
#include <json/nlohmann/json.hpp>
#include <log/csv.h>
#include <spdlog/version.h>
#endif

#ifdef PANGOLIN_DEVELOP
#include <pangolin/pangolin.h>
#endif

int main()
{
    std::cout << "Hello World!" << std::endl;

#ifdef OPENCV_DEVELOP
    std::cout << "OpenCV Version: " << CV_VERSION << std::endl;
#endif

#ifdef EIGEN_DEVELOP
    std::cout << "Eigen Version: " << EIGEN_WORLD_VERSION << "." << EIGEN_MAJOR_VERSION << "." << EIGEN_MINOR_VERSION << std::endl;
#endif

#ifdef PCL_DEVELOP
    std::cout << "PCL(Point Cloud Libarry) Version: " << PCL_VERSION_PRETTY << std::endl;
#endif

#ifdef CERES_DEVELOP
    std::cout << "Ceres-solver Version: " << CERES_VERSION_STRING << std::endl;
#endif

#ifdef GTSAM_DEVELOP
    std::cout << "GTSAM Version: " << GTSAM_VERSION_STRING << std::endl;
#endif

#ifdef PANGOLIN_DEVELOP
    std::cout << "Pangolin Version: " << PANGOLIN_VERSION_STRING << std::endl;
#endif

#ifdef SPDLOG_DEVELOP
    std::cout << "spdlog Version: " << SPDLOG_VER_MAJOR << "." << SPDLOG_VER_MINOR << "." << SPDLOG_VER_PATCH << std::endl;

    io::CSVReader<3> reader("./resource/sampleCSV.csv");
    std::string first, second, third;
    while (reader.read_row(first, second, third))
        std::cout << first << second << " " << third << std::endl;

    std::ifstream file("./resource/sampleJSON.json");
    nlohmann::json j;
    file >> j;
    std::vector<std::string> keys = { "first", "second", "third" };
    std::string str;
    for (const auto& key : keys)
        str += j[key];
    std::cout << str << std::endl;
#endif

    return 0;
}
