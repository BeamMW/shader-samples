cmake_minimum_required(VERSION 3.18)

add_library(shader-lib shader_lib.cpp)

target_include_directories(shader-lib PUBLIC "${CMAKE_SOURCE_DIR}/beam/bvm")

export(TARGETS shader-lib NAMESPACE Beam:: FILE ${CMAKE_SOURCE_DIR}/cmake/ShaderLib.cmake)
