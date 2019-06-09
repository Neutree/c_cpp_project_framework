############### Add include ###################
list(APPEND ADD_INCLUDE "include"
    )
list(APPEND ADD_PRIVATE_INCLUDE "")
###############################################

############ Add source files #################
list(APPEND ADD_SRCS  "src/main.c"
                      "src/test.c"
    )
# aux_source_directory(src ADD_SRCS)
# list(REMOVE_ITEM COMPONENT_SRCS "src/test2.c")
###############################################


register_component()

