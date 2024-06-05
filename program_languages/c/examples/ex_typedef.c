#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// This is not large enough to hold some of the strings. This will give a warning when compiled.
// Furthermore, some of the outputs will be truncated, and the outputs will look funny.
// Because of this, it is important to use strncpy to copy the string into the array rather than strcpy to avoid buffer overflow.

#define SIZE 10

typedef char LL[SIZE]; // defines LL as an array of SIZE characters

int main(){

    LL* abc_typedef; // abc_typedef is a pointer to an array of SIZE characters
    // this is the same as the following
    char (*abc)[SIZE] = NULL; // abc is a pointer to an array of SIZE characters
    if (abc == NULL) {
        printf("abc is NULL\n");
    }
    
    // Allocate memory for abc_typedef
    abc_typedef = (LL*)malloc(sizeof(LL));
    
    strncpy(*abc_typedef, "Hello World", sizeof(LL));

    printf("abc_typedef: %s\n", *abc_typedef);

    free(abc_typedef);    

    // Allocate memory for an array of SIZE characters
    LL* ll1 = (LL*)calloc(4, sizeof(LL));
    strncpy(ll1[0], "Hello One", sizeof(LL));
    strncpy(ll1[1], "Hello Two", sizeof(LL));
    strncpy(ll1[2], "Hello Three", sizeof(LL));
    strncpy(ll1[3], "Hello Four", sizeof(LL));
    printf("ll1: %s\n", ll1[0]);
    printf("ll2: %s\n", ll1[1]);
    printf("ll3: %s\n", ll1[2]);
    printf("ll4: %s\n", ll1[3]);
    free(ll1);

    return 0; 
}