project(mux)

set(MUX_DIR ${SRC_DIR}/base/mux)

add_executable(test_onehot_mux ${TEST_DIR}/test.cpp test_onehot_mux.cpp
                               OneHotMuxWrapper.cpp)
target_include_directories(test_onehot_mux PRIVATE ${TEST_DIR})
target_link_libraries(test_onehot_mux PRIVATE Catch2::Catch2)
verilate(
  test_onehot_mux
  SOURCES
  ${MUX_DIR}/onehot_mux.sv
  INCLUDE_DIRS
  ${INCLUDE_DIR}
  TRACE
  VERILATOR_ARGS
  --vpi)
catch_discover_tests(test_onehot_mux)
