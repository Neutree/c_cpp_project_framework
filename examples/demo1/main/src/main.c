
#include "stdio.h"
#include "test.h"
#include "lib2.h"
// #include "lib2_private.h"  // We can't include lib2_private.h for it's compoent2's private include dir

int main()
{
    printf("hello\n");
    test();
    lib2_test();
    return 0;
}

