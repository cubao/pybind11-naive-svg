cmake_minimum_required(VERSION 3.4...3.18)
project(naive_svg)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_CXX_STANDARD 14)

include_directories(headers/include)

set(PYBIND11_CPP_STANDARD -std=c++14)
add_subdirectory(pybind11)
file(GLOB SRCS src/*.cpp)
pybind11_add_module(_naive_svg ${SRCS})

# EXAMPLE_VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
target_compile_definitions(_naive_svg
                           PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})
