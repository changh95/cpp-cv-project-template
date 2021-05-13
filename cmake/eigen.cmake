# Eigen

find_package (Eigen3 PATHS ${CMAKE_CURRENT_SOURCE_DIR}/third_party/Eigen/install)
if (${Eigen3_FOUND})
	message(STATUS "Found Eigen3")
	add_definitions(-DEIGEN_DEVELOP)

    include_directories(
        ${Eigen3_INCLUDE_DIRS}
    )

    set(EIGEN_LIBS Eigen3::Eigen)
else (${Eigen3_FOUND})
	message(STATUS "Could not support Eigen3")
endif (${Eigen3_FOUND})