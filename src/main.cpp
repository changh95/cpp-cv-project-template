#include <iostream>

#ifdef OPENCV_DEVELOP
#include <opencv2/core.hpp>
#endif

#ifdef PCL_DEVELOP
#include <pcl/pcl_base.h>
#include <pcl/pcl_config.h>
#endif

int main()
{
    std::cout << "Hello World!" << std::endl;

#ifdef OPENCV_DEVELOP
    std::cout << "OpenCV Version: " << CV_VERSION << std::endl;
#endif

#ifdef PCL_DEVELOP
    std::cout << "PCL(Point Cloud Libarry) Version: " << PCL_VERSION_PRETTY << std::endl;
#endif

    return 0;
}