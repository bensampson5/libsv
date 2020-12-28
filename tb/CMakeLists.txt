add_executable(Vcounter test_counter.cpp)
verilate(Vcounter SOURCES ../src/counter.sv)

add_executable(Vcounter2 test_counter2.cpp catch_amalgamated.cpp)
verilate(Vcounter2 SOURCES ../src/counter.sv)

add_executable(foo foo.cpp catch_amalgamated.cpp)

# add_executable(foo test.cpp)
# target_link_libraries(foo PRIVATE Catch2::Catch2)