# Utilities - spdlog, fast-cpp-csv-parser

# csv reader dependency
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)
set(THREAD_LIBS Threads::Threads)

message(STATUS "Finding spdlog... checking ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/spdlog/install")
find_package (spdlog PATHS ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/spdlog/install)
if (${spdlog_FOUND})
	message(STATUS "Found spdlog")
	add_definitions(-DSPDLOG_DEVELOP)

    include_directories(
        ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/spdlog/install/include
    )

    set(SPDLOG_LIBS spdlog::spdlog)

else (${spdlog_FOUND})
	message(STATUS "Could not support spdlog")
endif (${spdlog_FOUND})