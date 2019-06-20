################# Add include #################
list(APPEND ADD_INCLUDE "include"
    )
# list(APPEND ADD_PRIVATE_INCLUDE "include_private")
###############################################

############## Add source files ###############
list(APPEND ADD_SRCS  "src/lib1.c"
    )
# aux_source_directory(src ADD_SRCS)
# list(REMOVE_ITEM COMPONENT_SRCS "src/test.c")
###############################################

###### Add required/dependent components ######
# list(APPEND ADD_REQUIREMENTS component1)
###############################################

############ Add static libs ##################
if(CONFIG_COMPONENT1_INCLUDE_STATIC_LIB)
    list(APPEND ADD_STATIC_LIB "lib/libtest.a")
endif()
###############################################

register_component()

