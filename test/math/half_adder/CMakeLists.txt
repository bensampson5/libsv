project(half_adder)

set(HALF_ADDER_DIR ${SRC_DIR}/math/half_adder)

add_executable(test_half_adder ${TEST_DIR}/test.cpp test_half_adder.cpp
                               HalfAdderWrapper.cpp)
target_include_directories(test_half_adder PRIVATE ${TEST_DIR})
target_link_libraries(test_half_adder PRIVATE Catch2::Catch2)
verilate(
  test_half_adder
  SOURCES
  ${HALF_ADDER_DIR}/half_adder.sv
  INCLUDE_DIRS
  ${INCLUDE_DIR}
  TRACE
  VERILATOR_ARGS
  --vpi)
catch_discover_tests(test_half_adder)