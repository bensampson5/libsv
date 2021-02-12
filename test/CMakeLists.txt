project(test)

# Get all test source files
file(GLOB_RECURSE TEST_SOURCE_FILES CONFIGURE_DEPENDS *.cpp)

add_executable(test_main ${TEST_SOURCE_FILES})
target_include_directories(test_main PRIVATE ${TEST_DIR})
target_link_libraries(test_main PRIVATE Catch2::Catch2)
verilate(test_main SOURCES ${SRC_DIR}/counter/counter.sv TRACE VERILATOR_ARGS
         --vpi)

include(CTest)
include(Catch)
catch_discover_tests(test_main)

add_custom_target(
  check
  COMMAND ${CMAKE_CTEST_COMMAND}
  DEPENDS test_main)

add_subdirectory(counter)
