add_executable(Vcounter test_counter.cpp)
verilate(Vcounter SOURCES ../src/counter.sv TRACE)