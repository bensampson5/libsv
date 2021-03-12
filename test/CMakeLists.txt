project(test)

include(CTest)
include(Catch)

add_subdirectory(base)

add_custom_target(check COMMAND ${CMAKE_CTEST_COMMAND})
