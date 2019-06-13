
#include "stdio.h"
#include "test.h"
#include "global_config.h"

#if CONFIG_COMPONENT2_ENABLED
#include "lib2.h"
#endif

// #include "lib2_private.h"  // We can't include lib2_private.h for it's compoent2's private include dir

int main()
{
    printf("hello\n");
    test();
#if CONFIG_COMPONENT2_ENABLED
    lib2_test();
#else
    printf("lib2 disabled\r\n");
#endif
    return 0;
}

