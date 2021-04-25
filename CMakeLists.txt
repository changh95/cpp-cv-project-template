cmake_minimum_required(VERSION 3.10)
project(
	"CV_Project"
	VERSION 0.1.0
	LANGUAGES C CXX
	)

# Standard CMake modules
include(CTest)
include(CMakeDependentOption)
include(GNUInstallDirs)
include(InstallRequiredSystemLibraries)
include(CMakePackageConfigHelpers)

# Custom modules and scripts
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DOR}/cmake")
#include(...)

set(CMAKE_CXX_STANDARD 17)
message(STATUS "-std=C++17")

set(CMAKE_CXX_FLAGS "-Wall -Wextra")
set(CMAKE_CXX_FLAGS "-O0")
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
message(STATUS "-Wall -Wextra -O0")

# 3rdParty dependencies
#add_subdirectory(third_party EXCLUDE_FROM_ALL)

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

# Source files
add_executable(CV_Project src/main.cpp)

target_link_libraries(CV_Project
	PRIVATE
	#general spdlog::spdlog
	)

# csv reader depdency
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

find_package (Eigen3 3.3 REQUIRED NO_MODULE)

message(STATUS )

find_package (OpenCV PATHS ${CMAKE_CURRENT_SOURCE_DIR}/third_party/opencv/install)
if (${OpenCV_FOUND})
	message(STATUS "Found OpenCV")
	add_definitions(-DOPENCV_DEVELOP)
else (${OpenCV_FOUND})
	message(STATUS "Could not support OpenCV")
endif (${OpenCV_FOUND})

find_package (PCL PATHS ${CMAKE_CURRENT_SOURCE_DIR}/third_party/pcl/install)
if (${PCL_FOUND})
	message(STATUS "Found PCL(Point Cloud Library)")
	add_definitions(-DPCL_DEVELOP)
else (${PCL_FOUND})
	message(STATUS "Could not support PCL(Point Cloud Library)")
endif (${PCL_FOUND})

set(BIN_FILE solution)
set(BIN_FOLDER_PATH bin/)
set(3RDPARTY_PATH 3rdParty/)

include_directories(
    include/
    include/fast-cpp-csv-parser/
    ${Eigen3_INCLUDE_DIRS}
	${OpenCV_INCLUDE_DIRS}
	${PCL_INCLUDE_DIRS}
)

add_executable(${BIN_FILE}
src/main.cpp
)

set_target_properties(${BIN_FILE} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${BIN_FOLDER_PATH})

target_link_libraries(
	${BIN_FILE}
	Eigen3::Eigen
	Threads::Threads
	${OpenCV_LIBS}
	${PCL_LIBS}
)