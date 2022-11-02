cmake_minimum_required(VERSION 3.15)

execute_process(
    COMMAND ${CMAKE_SOURCE_DIR}/scripts/run_conan_install.sh ${CMAKE_SOURCE_DIR} --output-folder ${CMAKE_BINARY_DIR}
)

set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/conanfile.py")
set(CMAKE_TOOLCHAIN_FILE "${CMAKE_BINARY_DIR}/conan_toolchain.cmake" CACHE PATH "Toolchain" FORCE)

project(conan-editable-test CXX)

add_executable(test src/test.cpp)

find_package(foo REQUIRED)
target_link_libraries(test PRIVATE foo::foo)
