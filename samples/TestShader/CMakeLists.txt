cmake_minimum_required(VERSION 3.18)

add_executable(TestShader test_contract.cpp)
target_link_libraries(TestShader PRIVATE shader-lib)
