project(test)

add_executable(test_main test.cpp ./counter/test_counter.cpp)
target_link_libraries(test_main PRIVATE Catch2::Catch2)
verilate(test_main SOURCES ${SRC_DIR}/counter/counter.sv TRACE VERILATOR_ARGS --vpi)

add_subdirectory(counter)