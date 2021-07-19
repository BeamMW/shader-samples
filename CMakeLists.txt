cmake_minimum_required(VERSION 3.18)

project(beam-shader-sdk)

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/beam/cmake" ${CMAKE_MODULE_PATH})


set(CMAKE_EXECUTABLE_SUFFIX .wasm)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -std=c++17 -flto -fno-rtti -Wno-inline-new-delete -fno-exceptions -nostartfiles ") #-nostdlib ")

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-invalid-noreturn")

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wl,--no-entry,--allow-undefined,--export=Ctor,--export=Dtor,--export=Method_2") #,--strip-all")

include_directories(beam/bvm)
add_subdirectory(shaderlib)
add_subdirectory(samples)