cmake_minimum_required(VERSION 3.17)

add_test_snippet(shader_test Beam::bvm Beam::beam)
target_include_directories(shader_test PUBLIC ${PROJECT_SOURCE_DIR}/shaders)


build_target(contract)
build_target(contract_header)
build_target(app)


add_dependencies(shader_test contract_header_build)
add_dependencies(app_build contract_header_build)
