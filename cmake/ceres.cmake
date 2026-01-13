# Ceres-solver

message(STATUS "Finding Ceres... checking ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/ceres/install")
find_package (Ceres PATHS ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/ceres/install)
if (${Ceres_FOUND})
	message(STATUS "Found Ceres")
	add_definitions(-DCERES_DEVELOP)

    include_directories(
        ${Ceres_INCLUDE_DIRS}
    )

    set(CERES_LIBS Ceres::ceres)

else (${Ceres_FOUND})
	message(STATUS "Could not support Ceres")
endif (${Ceres_FOUND})