# Shader SDK (work in progress)
This repository contains the samples of developement of shaders for Beam.
The aim of it is to make shaders developement more comfotable, at least for C++ developers. These samples use `wasi-sdk` which is based on `llvm libcxx`.
`shaderlib` folder contains a small piece of code to link standard C/C++ functions to Beam Virtual Machine calls. All samples should depend on `shaderlib`.
Finaly, `shaderlib` should became a C++ SDK for the shaders.

# How to use
* Install wasi-sdk from https://github.com/WebAssembly/wasi-sdk
* Generate build script
```
cmake -G "Ninja"
      -DCMAKE_BUILD_TYPE=Release
      -DCMAKE_TOOLCHAIN_FILE=<PATH_TO_WASI_SDK>/share/cmake/wasi-sdk.cmake 
      -DCMAKE_SYSROOT=<PATH_TO_WASI_SDK>/share/wasi-sysroot
      -DWASI_SDK_PREFIX=<PATH_TO_WASI_SDK>
      -DCMAKE_CXX_COMPILER_FORCED=True
      -DCMAKE_C_COMPILER_FORCED=True
      .
```
* Add a new folder for the new shader to the root directory
* Copy the content of `TestShader` into the new folder
* Update `CMakelists.txt` file with
```
    add_subdirectory(<Your shader folder>)
```
* Please, enjoy and let me know about any problems:)
