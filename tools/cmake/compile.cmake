
# Convert to cmake path(for Windows)
file(TO_CMAKE_PATH "${SDK_PATH}" SDK_PATH)

message(STATUS "SDK_PATH:${SDK_PATH}")

get_filename_component(parent_dir ${CMAKE_PARENT_LIST_FILE} DIRECTORY)
get_filename_component(current_dir ${CMAKE_CURRENT_LIST_FILE} DIRECTORY)
get_filename_component(parent_dir_name ${parent_dir} NAME)

function(register_component)
    get_filename_component(component_dir ${CMAKE_CURRENT_LIST_FILE} DIRECTORY)
    get_filename_component(component_name ${component_dir} NAME)
    message(STATUS "register component: ==${component_name}==, path:${component_dir}")

    # Add src to lib
    if(ADD_SRCS)
        add_library(${component_name} STATIC ${ADD_SRCS})
        set(include_type PUBLIC)
    else()
        add_library(${component_name} INTERFACE)
        set(include_type INTERFACE)
    endif()

    # Add include
    foreach(include_dir ${ADD_INCLUDE})
        get_filename_component(abs_dir ${include_dir} ABSOLUTE BASE_DIR ${component_dir})
        if(NOT IS_DIRECTORY ${abs_dir})
            message(FATAL_ERROR "${CMAKE_CURRENT_LIST_FILE}: ${include_dir} not found!")
        endif()
        target_include_directories(${component_name} ${include_type} ${abs_dir})
    endforeach()

    # Add private include
    foreach(include_dir ${ADD_PRIVATE_INCLUDE})
        if(${include_type} STREQUAL INTERFACE)
            message(FATAL_ERROR "${CMAKE_CURRENT_LIST_FILE}: ADD_PRIVATE_INCLUDE set but no source file！")
        endif()
        get_filename_component(abs_dir ${include_dir} ABSOLUTE BASE_DIR ${component_dir})
        if(NOT IS_DIRECTORY ${abs_dir})
            message(FATAL_ERROR "${CMAKE_CURRENT_LIST_FILE}: ${include_dir} not found!")
        endif()
        target_include_directories(${component_name} PRIVATE ${abs_dir})
    endforeach()
    target_link_libraries(${component_name} ${ADD_REQUIREMENTS})
endfunction()

macro(project name)
    
    _project(${name} ASM C CXX)

    # Find components, register components
    add_subdirectory(${SDK_PATH}/components/component1 component1)
    add_subdirectory(${SDK_PATH}/components/component2 component2)
    add_subdirectory(${SDK_PATH}/examples/demo1/main main)

    # Create exe_src.c to satisfy cmake's `add_executable` interface!
    set(exe_src ${CMAKE_BINARY_DIR}/exe_src.c)
    add_executable(${name} "${exe_src}")
    add_custom_command(OUTPUT ${exe_src} COMMAND ${CMAKE_COMMAND} -E touch ${exe_src} VERBATIM)
    add_custom_target(gen_exe_src DEPENDS "${exe_src}")
    add_dependencies(${name} gen_exe_src)
    target_link_libraries(${name} main)
endmacro()

