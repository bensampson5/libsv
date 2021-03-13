project(mux)

set(MUX_DIR ${SRC_DIR}/base/mux)

add_executable(test_mux ${TEST_DIR}/test.cpp test_mux.cpp MuxWrapper.cpp)
target_include_directories(test_mux PRIVATE ${TEST_DIR})
target_link_libraries(test_mux PRIVATE Catch2::Catch2)
verilate(
  test_mux
  SOURCES
  ${MUX_DIR}/mux.sv
  INCLUDE_DIRS
  ${INCLUDE_DIR}
  TRACE
  VERILATOR_ARGS
  --vpi)
catch_discover_tests(test_mux)
