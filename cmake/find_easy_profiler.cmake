message(STATUS "Finding Easy-profiler...")

find_package(easy_profiler REQUIRED HINTS ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/easy_profiler/install/Release/lib/cmake/easy_profiler)

if(${easy_profiler_FOUND})
  message(STATUS "Found: Easy-profiler - ${easy_profiler_INCLUDE_DIRS}")

  include_directories(${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/easy_profiler/install/Release/include)
  set(EASY_PROFILER_LIBS easy_profiler)
endif(${easy_profiler_FOUND})

set(BUILD_WITH_EASY_PROFILER true)