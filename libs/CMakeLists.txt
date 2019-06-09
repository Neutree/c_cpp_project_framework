
aux_source_directory(lib2 DIR_LIBS_SRCS)


option (USE_MYMATH2
       "Use provided math implementation" ON)


add_library(libs ${DIR_LIBS_SRCS})
