
#include "lib1.h"
#include "lib2.h"
#include "lib2_private.h"
#include "stdio.h"
#include "global_config.h"


void lib2_test()
{
    printf("lib2_test\r\n");
#ifdef CONFIG_COMPONENT2_TEST_STR1    
    printf("lib2 test string 1\r\n");
#elif defined CONFIG_COMPONENT2_TEST_STR2
    printf("lib2 test string 2\r\n");
#elif defined CONFIG_COMPONENT2_TEST_STR3
    printf("lib2 test string 3\r\n");
#endif
}

