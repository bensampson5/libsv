project(test)

include(CTest)
include(Catch)

add_subdirectory(core)
add_subdirectory(math)

add_custom_target(check COMMAND ${CMAKE_CTEST_COMMAND})
