message(STATUS "Finding OpenCV...")

if (CMAKE_BUILD_TYPE MATCHES "Debug")
  find_package(OpenCV REQUIRED HINTS ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/opencv/install/Debug/lib/cmake/opencv4)
endif (CMAKE_BUILD_TYPE MATCHES "Debug")

if (CMAKE_BUILD_TYPE MATCHES "Release")
  find_package(OpenCV REQUIRED HINTS ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/opencv/install/Release/lib/cmake/opencv4)
endif (CMAKE_BUILD_TYPE MATCHES "Release")

if (OpenCV_FOUND)
  message(STATUS "Found OpenCV library: " ${OpenCV_INCLUDE_DIRS})

  include_directories(${OpenCV_INCLUDE_DIRS})

  # OpenCV already defined its libraries as ${OpenCV_LIBS}
endif (OpenCV_FOUND)
