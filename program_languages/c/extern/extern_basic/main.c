#include <stdio.h>

// this global variable is defined somewhere else that will be linked
extern int global_var;

int main() {
    printf("Global variable: %d\n", global_var);
    return 0;
}