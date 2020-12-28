cmake_minimum_required(VERSION 3.16)

project(ip_catalog)
find_package(verilator HINTS $ENV{VERILATOR_ROOT})

add_subdirectory(tb)