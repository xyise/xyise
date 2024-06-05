#include <iostream>

// bring a C function into C++ code
extern "C"
{
    void hello_from_c();
}

// Or, get all function in h
// extern "C"
// {
// #include "c_library.h"
// }

int main()
{
    hello_from_c();
    return 0;
}