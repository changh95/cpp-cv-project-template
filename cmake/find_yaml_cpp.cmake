message(STATUS "Finding yaml-cpp...")

find_package(yaml-cpp REQUIRED HINTS ${CMAKE_SOURCE_DIR}/thirdparty/yaml_cpp/install/Release/share/cmake/yaml-cpp)

if (yaml-cpp_FOUND)
    message(STATUS "Found yaml-cpp - ${yaml-cpp_DIR}")

    include_directories(${yaml-cpp_INCLUDE_DIRS})
    include_directories(${CMAKE_SOURCE_DIR}/thirdparty/yaml_cpp/install/Release/include)
    include_directories(/opt/homebrew/opt/yaml-cpp/include)

    set(YAML_CPP_LIBS yaml-cpp)

endif (yaml-cpp_FOUND)

# find_library(YAML_CPP_LIB NAMES yaml-cpp PATHS ${SEARCH_LIBS})
# find_path(YAML_CPP_INCLUDE NAMES yaml-cpp/yaml.h PATHS ${SEARCH_HEADERS})
# if (YAML_CPP_INCLUDE)
#   message("-- Found yaml-cpp: " ${YAML_CPP_INCLUDE})
# endif (YAML_CPP_INCLUDE)
