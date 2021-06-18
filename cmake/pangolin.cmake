# Pangolin

find_package (Pangolin PATHS ${CMAKE_CURRENT_SOURCE_DIR}/third_party/pangolin/install)
if (${Pangolin_FOUND})
	message(STATUS "Found Pangolin")
	add_definitions(-DPANGOLIN_DEVELOP)

    include_directories(
        ${PANGOLIN_INCLUDE_DIRS}
    )

else (${Pangolin_FOUND})
	message(STATUS "Could not support Pangolin")
endif (${Pangolin_FOUND})
