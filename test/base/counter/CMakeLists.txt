project(counter)

add_executable(test_counter ${TEST_DIR}/test.cpp test_counter.cpp
                            CounterWrapper.cpp)
target_include_directories(test_counter PRIVATE ${TEST_DIR})
target_link_libraries(test_counter PRIVATE Catch2::Catch2)
verilate(test_counter SOURCES ${SRC_DIR}/base/counter/counter.sv TRACE
         VERILATOR_ARGS --vpi)
catch_discover_tests(test_counter)
