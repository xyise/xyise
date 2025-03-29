#include <stdio.h>

int main()
{
    char x2[5];
    printf("sizeof(x) = %lu\n", sizeof(x2));

    double x[] = {1.1, 2.2, 3.3, 4.4, 5.5};
    printf("sizeof(x) = %lu\n", sizeof(x));

    return 0;
}