cmake_minimum_required(VERSION 3.12)

project(openhdl LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED)

get_filename_component(SRC_DIR src ABSOLUTE)

find_package(verilator REQUIRED)
find_package(Catch2 REQUIRED)

include_directories(include)
add_subdirectory(test)

enable_testing()