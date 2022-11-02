cmake_minimum_required(VERSION 3.15)
project(foo CXX)

add_library(foo STATIC src/foo.cpp)
set_target_properties(foo PROPERTIES PUBLIC_HEADER include/foo.h)

find_package(hello REQUIRED)
target_link_libraries(foo PUBLIC hello::hello)

install(TARGETS foo)
