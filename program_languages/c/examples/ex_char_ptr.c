#include <stdio.h> 
#include <string.h>


int main()
{
    char *c = "";
    char nul = '\0';
    char *z = NULL;
    int zero = 0;

    if(c)
        printf("c is 'true'.\n");

    if(z)
        printf("z is 'true'.\n");

    if(c == NULL)
        printf("c is NULL.\n");

    if(z == (void *)zero)
        printf("z == zero.\n");

    if(!strcmp(c, &nul))
        printf("c is the same as a null character.\n");

    if(!strcmp(c,z))
        printf("c is the same as z.\n");

    return 0;
}
