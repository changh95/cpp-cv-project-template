message(STATUS "Finding Pangolin...")

# TODO(Hyunggi): Pangolin may need to be optional, since we only need Pangolin to qualitatively assess SLAM algorithms.

if (CMAKE_BUILD_TYPE MATCHES "Debug")
  find_package(Eigen3 REQUIRED HINTS ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/eigen/install/Debug/share/eigen3/cmake)
  find_package(Pangolin REQUIRED HINTS ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/pangolin/install/Debug/lib/cmake/Pangolin)
endif (CMAKE_BUILD_TYPE MATCHES "Debug")

if (CMAKE_BUILD_TYPE MATCHES "Release")
  find_package(Eigen3 REQUIRED HINTS ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/eigen/install/Release/share/eigen3/cmake)
  find_package(Pangolin REQUIRED HINTS ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/pangolin/install/Release/lib/cmake/Pangolin)
endif (CMAKE_BUILD_TYPE MATCHES "Release")

# find_library(PANGOLIN_LIB NAMES pangolin PATHS ${SEARCH_LIBS})
# find_path(PANGOLIN_INCLUDE NAMES pangolin.h PATHS ${SEARCH_HEADERS})

if (${Pangolin_FOUND})
  message(STATUS "Found Pangolin - ${Pangolin_INCLUDE_DIRS}")

  include_directories(${Pangolin_INCLUDE_DIRS})
  set(PANGOLIN_LIBS ${Pangolin_LIBRARIES})

else (${Pangolin_FOUND})
	message(STATUS "Could not support Pangolin")
endif (${Pangolin_FOUND})