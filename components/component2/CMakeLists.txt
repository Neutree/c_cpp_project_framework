# Config enable component2 or not in Kconfig
if(CONFIG_COMPONENT2_ENABLED)

    ################# Add include #################
    list(APPEND ADD_INCLUDE "include"
        )
    list(APPEND ADD_PRIVATE_INCLUDE "include_private")
    ###############################################

    ############## Add source files ###############
    list(APPEND ADD_SRCS  "src/lib2.c"
        )
    # aux_source_directory(src ADD_SRCS)
    # list(REMOVE_ITEM COMPONENT_SRCS "src/test.c")
    ###############################################

    ###### Add required/dependent components ######
    list(APPEND ADD_REQUIREMENTS component1)
    ###############################################
    
    ############ Add static libs ##################
    # list(APPEND ADD_STATIC_LIB "lib/libtest.a")
    ###############################################

    #### Add compile option for this component ####
    #### Just for this component, won't affect other 
    #### modules, including component that depend 
    #### on this component
    # add_definitions(-DAAAAA=1)
    # add_compile_options(-DAAAAA=1)
    ###############################################

    register_component()
endif()

