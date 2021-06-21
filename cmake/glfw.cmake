# GLFW

find_package(OpenGL)

find_package(glfw3 PATHS ${CMAKE_SOURCE_DIR}/third_party/glfw/install)

if (${GLFW_FOUND})
	message(STATUS "Found GLFW")
	add_definitions(-DGLFW_DEVELOP)

    include_directories(
        ${GLFW_INCLUDE_DIRS}
    )
    
    set(GLFW_LIBS glfw)

else (${GLFW_FOUND})
	message(STATUS "Could not support GLFW")
endif (${GLFW_FOUND})
