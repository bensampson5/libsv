add_executable(test_counter test.cpp test_counter.cpp)
target_link_libraries(test_counter PRIVATE Catch2::Catch2)
verilate(test_counter SOURCES ${SRC_DIR}/core/counter.sv VERILATOR_ARGS --vpi)

add_executable(test_main test.cpp test_counter.cpp)
target_link_libraries(test_main PRIVATE Catch2::Catch2)
verilate(test_main SOURCES ${SRC_DIR}/core/counter.sv VERILATOR_ARGS --vpi)