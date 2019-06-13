cmake_minimum_required(VERSION 3.10)


execute_process(COMMAND python3 --version RESULT_VARIABLE cmd_res)
if(NOT ${cmd_res} EQUAL 0)
message(STATUS "ERROR")
endif()
execute_process(COMMAND python2 --version RESULT_VARIABLE cmd_res)
message(STATUS "${cmd_res} ---- ")


project(demo1)

add_executable(demo1 components/component1/src/lib1.c)

message(STATUS "=======${PROJECT_SOURCE_DIR} === ${PROJECT_BUILD_DIR}")

