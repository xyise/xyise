#include <stdio.h>

void print_me(double x[])
{
    int m = sizeof(x)/sizeof(x[0]);

    for(int i=0; i<m; i++)
    {
        printf("%f\n", x[i]);
    }

}

int main()
{
    double x[] = {1.1, 2.2, 3.3, 4.4, 5.5};
    print_me(x);
    return 0;
}