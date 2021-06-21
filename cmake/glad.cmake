# GLAD

find_package(OpenGL)

add_library(glad 
    ${CMAKE_CURRENT_SOURCE_DIR}/third_party/glad/install/include/glad/glad.h 
    ${CMAKE_CURRENT_SOURCE_DIR}/third_party/glad/install/src/glad.c
    )
include_directories(
        glad PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/third_party/glad/install/include/
    )