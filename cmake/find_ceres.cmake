message(STATUS "Finding Ceres...")

if (CMAKE_BUILD_TYPE MATCHES "Debug")
  find_package(Eigen3 REQUIRED HINTS ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/eigen/install/Debug/share/eigen3/cmake)
  find_package(Ceres REQUIRED HINTS ${CMAKE_SOURCE_DIR}/thirdparty/ceres/install/Debug/lib/cmake/Ceres)
endif (CMAKE_BUILD_TYPE MATCHES "Debug")

if (CMAKE_BUILD_TYPE MATCHES "Release")
  find_package(Eigen3 REQUIRED HINTS ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/eigen/install/Release/share/eigen3/cmake)
  find_package(Ceres REQUIRED HINTS ${CMAKE_SOURCE_DIR}/thirdparty/ceres/install/Release/lib/cmake/Ceres)
endif (CMAKE_BUILD_TYPE MATCHES "Release")

if (${Ceres_FOUND})

  # According to http://ceres-solver.org/installation.html?highlight=include_directories, since v2.0 there is no ${CERES_INCLUDE_DIRS}
  # include_directories(${Ceres_INCLUDE_DIRS})

  # v1.14.0
  include_directories(${CERES_INCLUDE_DIRS})
  set(CERES_LIBS ${CERES_LIBRARIES})

endif (${Ceres_FOUND})
