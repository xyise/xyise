#include <iostream>
#include <vector>
#include <algorithm>
#include <string>

int main()
{
    std::string name = "Lambda";
    std::vector<int> numbers = {10, 21, 30, 41, 50};

    constexpr auto printNumber = [](int number) constexpr {
        std::cout << number << std::endl;
    };

    std::for_each(numbers.begin(), numbers.end(), printNumber);

    int sum = 0;
    std::for_each(numbers.begin(), numbers.end(), [&sum](int number){
        sum += number;
    });
    std::cout << "Sum: " << sum << std::endl;

    std::vector<int> evenNumbers;
    std::copy_if(numbers.begin(), numbers.end(), std::back_inserter(evenNumbers), [](int number){
        return number % 2 == 0;
    });

    std::fill_n(std::back_inserter(evenNumbers), 3, 0);
    for (int num: evenNumbers)
    {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    return 0;
}