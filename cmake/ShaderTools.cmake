cmake_minimum_required(VERSION 3.17)

function(generate_sid shader_target)
    add_custom_target(${shader_target}_header
        ALL
        COMMAND ${BEAM_SHADER_SDK}/bin/generate-sid $<TARGET_FILE:${shader_target}> > $<TARGET_PROPERTY:${shader_target},SOURCE_DIR>/contract_sid.i
        COMMENT "Generating SID for ${shader_target}..."
        VERBATIM
    )
endfunction()

function(generate_sid_for_file shader source_path path)
    add_custom_target(${shader}_header
        ALL
        COMMAND ${BEAM_SHADER_SDK}/bin/generate-sid ${source_path}/${shader}.wasm > ${path}/contract_sid.i
        COMMENT "Generating SID for ${shader}..."
        DEPENDS ${shader}_build
        VERBATIM
    )
endfunction()
