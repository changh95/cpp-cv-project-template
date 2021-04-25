# GTSAM

find_package (GTSAM PATHS ${CMAKE_CURRENT_SOURCE_DIR}/third_party/GTSAM/install)
if (${GTSAM_FOUND})
	message(STATUS "Found GTSAM")
	add_definitions(-DGTSAM_DEVELOP)

    include_directories(
        ${GTSAM_INCLUDE_DIRS}
    )
    
    set(GTSAM_LIBS gtsam)

else (${GTSAM_FOUND})
	message(STATUS "Could not support GTSAM")
endif (${GTSAM_FOUND})