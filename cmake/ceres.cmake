# Ceres-solver

find_package (Ceres PATHS ${CMAKE_CURRENT_SOURCE_DIR}/third_party/ceres-solver/install)
if (${Ceres_FOUND})
	message(STATUS "Found Ceres-solver")
	add_definitions(-DCERES_DEVELOP)

    include_directories(
        ${Ceres_INCLUDE_DIRS}
    )

    set(CERES_LIBS Ceres::ceres)

else (${Ceres_FOUND})
	message(STATUS "Could not support Ceres-solver")
endif (${Ceres_FOUND})