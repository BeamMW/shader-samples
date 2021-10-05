cmake_minimum_required(VERSION 3.17)

include(GenerateSID)

add_executable(TestShader test_contract.cpp)
target_link_libraries(TestShader PRIVATE shader-lib)

generate_sid_header(TestShader)

