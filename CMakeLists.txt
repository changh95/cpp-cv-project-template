cmake_minimum_required(VERSION 3.10)
project(Project)

set(CMAKE_CXX_STANDARD 17)
message(STATUS "-std=C++17")

set(CMAKE_CXX_FLAGS "-Wall -Wextra")
set(CMAKE_CXX_FLAGS "-O0")
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
message(STATUS "-Wall -Wextra -O0")

# csv reader depdency
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

find_package (Eigen3 3.3 REQUIRED NO_MODULE)

set(BIN_FILE solution)
set(BIN_FOLDER_PATH bin/)
set(3RDPARTY_PATH 3rdParty/)

include_directories(
    include/
    include/fast-cpp-csv-parser/
    ${Eigen3_INCLUDE_DIRS}
)

add_executable(${BIN_FILE} 
src/main.cpp
)
set_target_properties(${BIN_FILE} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${BIN_FOLDER_PATH})

target_link_libraries(${BIN_FILE} 
Eigen3::Eigen
Threads::Threads)
