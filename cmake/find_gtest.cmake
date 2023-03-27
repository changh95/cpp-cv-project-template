message(STATUS "Finding GTest...")

find_package(Threads REQUIRED)
find_package(GTest CONFIG REQUIRED HINTS ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/gtest/install/Release/lib/cmake/GTest)

if(GTest_FOUND)
  message(STATUS "Found GTest - ${GTEST_INCLUDE_DIRS}")

  include_directories(${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/gtest/install/Release/include)
  set(GTEST_LIBS GTest::gtest)

endif(GTest_FOUND)