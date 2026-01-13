#include <fstream>
#include <iostream>

#include <Eigen/Dense>
#include <ceres/ceres.h>
#include <opencv2/core.hpp>
#include <pcl/pcl_base.h>
#include <pcl/pcl_config.h>
#include <gtsam/global_includes.h>
#include <spdlog/version.h>


int main()
{
    std::cout << "Eigen Version: " << EIGEN_WORLD_VERSION << "." << EIGEN_MAJOR_VERSION << "." << EIGEN_MINOR_VERSION << std::endl;

    std::cout << "OpenCV Version: " << CV_VERSION << std::endl;

    std::cout << "Ceres-solver Version: " << CERES_VERSION_STRING << std::endl;

    std::cout << "PCL (Point Cloud Library) Version: " << PCL_VERSION_PRETTY << std::endl;

    std::cout << "GTSAM Version: " << GTSAM_VERSION_STRING << std::endl;

    std::cout << "spdlog Version: " << SPDLOG_VER_MAJOR << "." << SPDLOG_VER_MINOR << "." << SPDLOG_VER_PATCH << std::endl;

    return 0;
}
