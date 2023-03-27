option(BUILD_DOC "Build documentation" OFF)

if (BUILD_DOC)
   find_package(Doxygen REQUIRED)

   # set input and output files
   set(DOXYGEN_IN ${PROJECT_SOURCE_DIR}/docs/doxygen.in)
   set(DOXYGEN_OUT ${PROJECT_SOURCE_DIR}/docs/doxygen.out)

   message(STATUS "Config: Build Documentation - ON")

   # request to configure the file
   configure_file(${DOXYGEN_IN} ${DOXYGEN_OUT} @ONLY)

   # note the option ALL which allows to build the docs together with the application
   add_custom_target( doxygen ALL
            COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYGEN_OUT}
            WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
            COMMENT "Generating API documentation with Doxygen"
            VERBATIM ) 
endif(BUILD_DOC)