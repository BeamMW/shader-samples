cmake_minimum_required(VERSION 3.18)

add_executable(_INITIAL_CONTRACT_Contract contract.cpp)
add_executable(_INITIAL_CONTRACT_App app.cpp)
target_link_libraries(_INITIAL_CONTRACT_Contract PRIVATE shader-lib)
target_link_libraries(_INITIAL_CONTRACT_App PRIVATE shader-lib)
