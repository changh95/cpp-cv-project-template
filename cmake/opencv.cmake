# OpenCV

find_package (OpenCV PATHS ${CMAKE_CURRENT_SOURCE_DIR}/third_party/opencv/install)
if (${OpenCV_FOUND})
	message(STATUS "Found OpenCV")
	add_definitions(-DOPENCV_DEVELOP)

    include_directories(
        ${OpenCV_INCLUDE_DIRS}
    )

else (${OpenCV_FOUND})
	message(STATUS "Could not support OpenCV")
endif (${OpenCV_FOUND})

if (${OpenCV_FOUND})
	set(opencv_libs ${OPENCV_LIBS})
endif (${OpenCV_FOUND})