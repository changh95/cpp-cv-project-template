#include <iostream>

#ifdef OPENCV_DEVELOP
#include <opencv2/core.hpp>
#endif

int main()
{
	std::cout << "Hello World!" << std::endl;

	#ifdef OPENCV_DEVELOP
	std::cout << "OpenCV Version: " << CV_VERSION << std::endl;
	#endif

	return 0;
}
