
#include "lib1.h"
#include "stdio.h"
#include "global_config.h"

#include "math.h"
// need math lib named libm, we need to add `list(APPEND ADD_REQUIREMENTS m)` in CmakeLists.txt

static float math_exp(float x)
{
    return expf(x);
}

void test1()
{
    float x = 1.23;
    printf("lib1 test1: e^%f = %f\n", x, math_exp(x));
    #if AAAAA
    printf("AAAAAA\n");
    #endif
    #if AAAAA222
    printf("AAAAAA222\n");
    #endif

}

