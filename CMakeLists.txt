cmake_minimum_required(VERSION 3.12)

project(openhdl LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED)

include(cmake/CPM.cmake)

cpmaddpackage(
  NAME
  Format.cmake
  VERSION
  1.6
  GITHUB_REPOSITORY
  TheLartians/Format.cmake
  OPTIONS # enable cmake formatting (optional)
  "FORMAT_CHECK_CMAKE ON"
  # path to exclude (optional, supports regular expressions)
  "CMAKE_FORMAT_EXCLUDE cmake/CPM.cmake")

get_filename_component(SRC_DIR src ABSOLUTE)
get_filename_component(TEST_DIR test ABSOLUTE)
get_filename_component(INCLUDE_DIR include ABSOLUTE)

find_package(verilator REQUIRED)
find_package(Catch2 REQUIRED)

add_subdirectory(test)

enable_testing()
