#include <iostream>

#ifdef OPENCV_DEVELOP
#include <opencv4/opencv2/core.hpp>
#endif

int main()
{
	std::cout << "Hello World!" << std::endl;

	#ifdef OPENCV_DEVELOP
	std::cout << "OpenCV Version: " << cv::getVersionString() << std::endl;
	#endif

	return 0;
}
