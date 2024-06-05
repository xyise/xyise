#include <iostream>

constexpr int square(int x) {
    return x * x;
}

constexpr int cube(int x) {
    return x * x * x;
}

int main() {
    constexpr int num1 = square(5);
    constexpr int num2 = cube(3);

    std::cout << "Square of 5: " << num1 << std::endl;
    std::cout << "Cube of 3: " << num2 << std::endl;

    return 0;
}