
#include <cassert>
#include <iostream>
#include <map>
#include <string>
#include <variant>

int main()
{
    std::variant<int, double, std::string, std::map<std::string, double>> v, w;

    v = 12.0;
    w = 1.0;

    std::cout << std::get<double>(v) << std::endl;
    std::cout << std::get<std::string>(w) << std::endl;

    std::holds_alternative<int>(v);
    
    // v = 12; // v contains int
    // int i = std::get<int>(v);
    // assert(12 == i);

    // w = std::get<int>(v);
    // std::cout << std::get<int>(w) << std::endl;

    // v = std::string("abc"); // v contains std::string

    // if (std::holds_alternative<std::string>(v))
    // {
    //     std::cout << std::get<std::string>(v) << '\n'; // prints "abc"
    // }

    return 0;
}