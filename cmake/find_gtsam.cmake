message(STATUS "Finding GTSAM...")

if (CMAKE_BUILD_TYPE MATCHES "Debug")
  find_package(GTSAM REQUIRED HINTS ${CMAKE_SOURCE_DIR}/thirdparty/gtsam/install/Debug/lib/cmake)
endif (CMAKE_BUILD_TYPE MATCHES "Debug")

if (CMAKE_BUILD_TYPE MATCHES "Release")
  find_package(GTSAM REQUIRED HINTS ${CMAKE_SOURCE_DIR}/thirdparty/gtsam/install/Release/lib/cmake)
endif (CMAKE_BUILD_TYPE MATCHES "Release")

if(${GTSAM_FOUND})
  message(STATUS "Found: GTSAM - ${GTSAM_INCLUDE_DIRS}")

  include_directories(${GTSAM_INCLUDE_DIRS})
  set(GTSAM_LIBS gtsam)
endif(${GTSAM_FOUND})
