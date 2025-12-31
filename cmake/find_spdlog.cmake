message(STATUS "Finding spdlog...")

# csv reader dependency
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)
set(THREAD_LIBS Threads::Threads)

find_package(spdlog CONFIG REQUIRED HINTS ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/spdlog/install/Release/lib/cmake/spdlog)

if(spdlog_FOUND)
  message(STATUS "Found Spdlog - ${spdlog_INCLUDE_DIRS}")

  include_directories(${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/spdlog/install/Release/include)

  set(SPDLOG_LIBS spdlog::spdlog)

endif(spdlog_FOUND)