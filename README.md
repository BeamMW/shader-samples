# Get started
* Install `shader-sdk`, on Windows you should run these commands in `Developer Command Prompt for VS`
```bash
git clone https://github.com/BeamMW/shader-sdk.git
cd shader-sdk
```
On Linux and MacOS
```bash
./shade init
```
On Windows 
```bash
shade init
```
* Create envoronment valiable `BEAM_SHADER_SDK=<path to shader-sdk>`
* Create envoronment valiable `WASI_SDK_PREFIX=<path to wasi-sdk>`. `wasi-sdk` should exist in `shader-sdk` folder after `./shade init` command completion 
* Generate new shader project
```bash
mkdir new_project
cd new_project
<BEAM_SHADER_SDK>/shade create_project <project_name>
```
This script generate new project files where <project_name> is used for namespace, also it verifies that it compiles

* Build project

On Linux and MacOS
```bash
cmake -G "Ninja"
      -DCMAKE_BUILD_TYPE=Release
      -DCMAKE_TOOLCHAIN_FILE=$WASI_SDK_PREFIX/share/cmake/wasi-sdk.cmake 
      -DCMAKE_SYSROOT=$WASI_SDK_PREFIX/share/wasi-sysroot
      -DWASI_SDK_PREFIX=$WASI_SDK_PREFIX
      -DCMAKE_CXX_COMPILER_FORCED=True
      -DCMAKE_C_COMPILER_FORCED=True
      .
make
```
On Window
1. Open `new_project` folder in VS as a CMake project.
1. Choose configuration `wasm32-Release`
1. Build


# Learn about shaders
* [Overview](https://github.com/BeamMW/shader-sdk/wiki/Beam-Confidential-DeFi-Platform)
* [Introducing Beam Shaders](https://github.com/BeamMW/shader-sdk/wiki/Beam-Smart-Contracts)
* [Building Shaders](https://github.com/BeamMW/shader-sdk/wiki/Building-Beam-Shaders)
* [Running Shaders using CLI wallet](https://github.com/BeamMW/shader-sdk/wiki/Running-Beam-Shaders-using-CLI-Wallet)
* [API](https://github.com/BeamMW/shader-sdk/wiki/BVM-functions-for-shaders)
