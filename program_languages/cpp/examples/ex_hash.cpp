#include <iostream>
#include <unordered_map>
#include <string>
#include <functional>

struct Person {
    std::string name;
    int age;

    // Define a hash function for Person objects
    friend std::size_t hash_value(const Person& p) {
        std::size_t seed = 0;
        std::hash<std::string> stringHasher;
        std::hash<int> intHasher;
        seed ^= stringHasher(p.name) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        seed ^= intHasher(p.age) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        return seed;
    }

    // Define an equality operator for Person objects
    friend bool operator==(const Person& lhs, const Person& rhs) {
        return lhs.name == rhs.name && lhs.age == rhs.age;
    }
};

int main() {
    // std::unordered_map<Person, std::string, std::hash<Person>, std::equal_to<Person>> personMap;

    // Person p1{"John", 25};
    // Person p2{"Jane", 30};

    // personMap[p1] = "John's entry";
    // personMap[p2] = "Jane's entry";

    // std::cout << "Value associated with p1: " << personMap[p1] << std::endl;
    // std::cout << "Value associated with p2: " << personMap[p2] << std::endl;

    return 0;
}