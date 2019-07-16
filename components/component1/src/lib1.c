
#include "lib1.h"
#include "stdio.h"
#include "global_config.h"

void test1()
{
    printf("lib1 test1\n");
    #if AAAAA
    printf("AAAAAA\n");
    #endif
    #if AAAAA222
    printf("AAAAAA222\n");
    #endif

}

