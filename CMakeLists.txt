cmake_minimum_required(VERSION 3.12)

project(openhdl)
find_package(verilator REQUIRED)
find_package(Catch2 REQUIRED)

get_filename_component(SRC_DIR src ABSOLUTE)

include_directories(include)
add_subdirectory(test)