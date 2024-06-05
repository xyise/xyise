#include <stdio.h>

void ccpp_macro_example() {
    #ifdef __cplusplus
        printf("C++ compiler detected\n");
    #endif

    #ifdef __STDC__
        printf("Standard C compiler detected\n");
    #endif

    #ifdef c_plusplus
        printf("C++ compiler detected\n"); 
    #endif
}

int main() {
    ccpp_macro_example();
    return 0;
}