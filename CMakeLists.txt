cmake_minimum_required(VERSION 3.18)

project(beam-shader-sdk)

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/beam/cmake" ${CMAKE_MODULE_PATH})
set(BEAM_PROJECT_SOURCE_DIR ${PROJECT_SOURCE_DIR}/beam CACHE INTERNAL "")
set(BEAM_PROJECT_BINARY_DIR ${PROJECT_BINARY_DIR}/beam CACHE INTERNAL "")

if (CMAKE_SYSTEM_NAME MATCHES "WASI")
    set(CMAKE_EXECUTABLE_SUFFIX .wasm)

    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -std=c++17 -flto -fno-rtti -Wno-inline-new-delete -fno-exceptions -nostartfiles ") #-nostdlib ")

    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-invalid-noreturn")

    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wl,--no-entry,--allow-undefined,--export=Ctor,--export=Dtor,--export=Method_2") #,--strip-all")

    include_directories(beam/bvm)
    add_subdirectory(shaderlib)
	#add_subdirectory(samples)
    add_subdirectory(shaders)
else()
    set(BEAM_BVM_ONLY TRUE)
    set(BEAM_ATOMIC_SWAP_SUPPORT FALSE)
    set(BEAM_WALLET_CLIENT_LIBRARY TRUE)
    set(BEAM_TESTS_ENABLED FALSE) 
    add_subdirectory(beam)

    # export beam targets to be able to use them from another folder
    # TODO: should be replaced with installation of the beam library
    export(
        TARGETS
            beam
            bvm
            core
            keccak
            ethash
            pbkdf
            p2p
            pow
            utility
            secp256k1
            blake2b
            uv_a
            generate-sid
        NAMESPACE Beam::
        FILE ${PROJECT_SOURCE_DIR}/cmake/Bvm.cmake)
endif()
