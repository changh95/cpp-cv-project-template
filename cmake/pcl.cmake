# PCL(Point Cloud Library)

find_package (PCL PATHS ${CMAKE_CURRENT_SOURCE_DIR}/third_party/pcl/install)
if (${PCL_FOUND})
	message(STATUS "Found PCL(Point Cloud Library)")
	add_definitions(-DPCL_DEVELOP)

    include_directories(
        ${PCL_INCLUDE_DIRS}
    )
    
else (${PCL_FOUND})
	message(STATUS "Could not support PCL(Point Cloud Library)")
endif (${PCL_FOUND})
