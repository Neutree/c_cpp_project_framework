
#include "lib1.h"
#include "lib2.h"
#include "lib2_private.h"
#include "stdio.h"
#include "global_config.h"
#include "global_build_info_time.h"
#include "global_build_info_version.h"


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
    printf("build time:%d-%d-%d %d:%d:%d\r\n", BUILD_TIME_YEAR, BUILD_TIME_MONTH,  BUILD_TIME_DAY,
                                         BUILD_TIME_HOUR, BUILD_TIME_MINUTE, BUILD_TIME_SECOND);
    printf("git info:v%d.%d.%d-%d %s \r\n", BUILD_VERSION_MAJOR, BUILD_VERSION_MINOR, BUILD_VERSION_MICRO,
                                            BUILD_VERSION_DEV, BUILD_GIT_COMMIT_ID);
    if(BUILD_VERSION_MAJOR == 0 &&
       BUILD_VERSION_MINOR == 0 &&
       BUILD_VERSION_MICRO == 0 &&
       BUILD_VERSION_DEV   == 0)
    {
        printf("no tag, create by command: git tag -a v0.1.1 -m \"release v0.1.1 describe.....\"\r\n");
    }
#if BUILD_GIT_IS_DIRTY
    printf("WARNING: git repository have file not commit when build\r\n");
#endif
    #if AAAAA
    printf("AAAAAA222222\n");
    #endif
}

