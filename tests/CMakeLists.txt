add_executable(test_counter test.cpp test_counter.cpp)
target_link_libraries(test_counter PRIVATE Catch2::Catch2)
verilate(test_counter SOURCES ${SRC_DIR}/counter.sv VERILATOR_ARGS --vpi)