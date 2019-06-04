
# cmake_minimum_required(VERSION 3.5)

# project(micropython C CXX ASM)

# SET(PROJECT_DIR maixpy)

# configure_file (
#   "${PROJECT_DIR}/config.h.in"
#   "${PROJECT_BINARY_DIR}/config.h"
# )

# option (USE_MYMATH
#        "Use provided math implementation" ON)

# set(REQUIRED_QT_VERSION 5.5.0)
# set(KF5_DEP_VERSION "5.28.0") # handled by release scripts

# find_package(Qt5 ${REQUIRED_QT_VERSION} NO_MODULE REQUIRED Gui)
# find_package(KF5Config ${KF5_DEP_VERSION} REQUIRED)

# find_package(KF5Config)
# add_subdirectory(libs)
# aux_source_directory(maixpy/src ROOT_SRCS)

# add_executable(demo ${ROOT_SRCS})
# target_link_libraries(demo KF5::ConfigCore KF5::ConfigGui)
# target_link_libraries(demo libs)


cmake_minimum_required(VERSION 3.5)
include(./tools/cmake/compile.cmake)
project(micropython)


