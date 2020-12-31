add_executable(test_main test.cpp ./core/test_counter.cpp)
target_link_libraries(test_main PRIVATE Catch2::Catch2)
verilate(test_main SOURCES ${SRC_DIR}/core/counter.sv VERILATOR_ARGS --vpi)

add_subdirectory(core)