message(STATUS "Finding PCL...")

if (CMAKE_BUILD_TYPE MATCHES "Debug")
  set(EIGEN_ROOT ${CMAKE_SOURCE_DIR}/thirdparty/eigen/install/Debug)
  find_package(Eigen3 REQUIRED HINTS ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/eigen/install/Debug/share/eigen3/cmake)
  find_package(PCL REQUIRED HINTS ${CMAKE_SOURCE_DIR}/thirdparty/pcl/install/Debug/share/pcl-1.13/)
endif (CMAKE_BUILD_TYPE MATCHES "Debug")

if (CMAKE_BUILD_TYPE MATCHES "Release")
  set(EIGEN_ROOT ${CMAKE_SOURCE_DIR}/thirdparty/eigen/install/Release)
  find_package(Eigen3 REQUIRED HINTS ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/eigen/install/Release/share/eigen3/cmake)
  find_package(PCL REQUIRED HINTS ${CMAKE_SOURCE_DIR}/thirdparty/pcl/install/Release/share/pcl-1.13/)
endif (CMAKE_BUILD_TYPE MATCHES "Release")

if(${PCL_FOUND})
  message(STATUS "Found: PCL - ${PCL_INCLUDE_DIRS}")
  include_directories(${PCL_INCLUDE_DIRS})
  set(PCL_LIBS ${PCL_LIBRARIES})
endif(${PCL_FOUND})
