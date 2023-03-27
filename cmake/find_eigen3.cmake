message(STATUS "Finding Eigen3...")

if (CMAKE_BUILD_TYPE MATCHES "Debug")
  find_package(Eigen3 REQUIRED HINTS ${CMAKE_SOURCE_DIR}/thirdparty/eigen/install/Debug/share/eigen3/cmake)
endif (CMAKE_BUILD_TYPE MATCHES "Debug")

if (CMAKE_BUILD_TYPE MATCHES "Release")
  find_package(Eigen3 REQUIRED HINTS ${CMAKE_SOURCE_DIR}/thirdparty/eigen/install/Release/share/eigen3/cmake)
endif (CMAKE_BUILD_TYPE MATCHES "Release")

# If not found, use Pkgconfig to find Eigen3 (But probably won't reach here...)
#if (NOT Eigen3_FOUND)
#  find_package(PkgConfig REQUIRED)
#  pkg_search_module(Eigen3 REQUIRED eigen3)
#endif(NOT Eigen3_FOUND)

if(${Eigen3_FOUND})
  message(STATUS "Found: Eigen3 - ${EIGEN3_INCLUDE_DIRS}")

  include_directories(${EIGEN3_INCLUDE_DIRS})
  set(EIGEN3_LIBS Eigen3::Eigen)
endif(${Eigen3_FOUND})
