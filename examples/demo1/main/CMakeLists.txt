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

###### Add required/dependent components ######
if(CONFIG_COMPONENT2_ENABLED)
    list(APPEND ADD_REQUIREMENTS component1 component2)
else()
    list(APPEND ADD_REQUIREMENTS component1)
endif()
###############################################

############ Add static libs ##################
# list(APPEND ADD_STATIC_LIB "lib/libtest.a")
###############################################


register_component()

